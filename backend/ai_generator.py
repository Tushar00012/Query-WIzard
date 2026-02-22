import os
import logging
import google.generativeai as genai
from deep_translator import GoogleTranslator
try:
    from . import db_config  # load .env at import-time (server only)
    from .schema_handler import load_schema, store_all_table_structures
except ImportError:
    import db_config
    from schema_handler import load_schema, store_all_table_structures

logging.basicConfig(level=logging.INFO)
translator = GoogleTranslator(source="auto", target="en")

# Secure flow: API key is set only on the backend server (e.g. GOOGLE_API_KEY in server env).
# Never accept or bundle the key in the client/desktop app.
def has_api_key():
    """True if the server has GOOGLE_API_KEY set (env only)."""
    return bool((os.getenv("GOOGLE_API_KEY") or "").strip())


def _ensure_genai_configured():
    api_key = (os.getenv("GOOGLE_API_KEY") or "").strip()
    if not api_key:
        return False
    genai.configure(api_key=api_key)
    return True


def _format_ai_error(exc: Exception) -> str:
    """Return a user-facing message. Never expose raw 403/leaked or API key details."""
    text = str(exc)
    lower = text.lower()
    if "403" in lower or "leak" in lower or "revoked" in lower:
        return "AI Error: Unable to generate SQL. Please try again later."
    if "api key" in lower and ("invalid" in lower or "not valid" in lower):
        return "AI Error: Unable to generate SQL. Please try again later."
    return f"AI Error: {text}"


def translate_to_english(text):
    """Translates input text to English while keeping table names intact."""
    try:
        return translator.translate(text)
    except Exception:
        return text


SQL_PROMPT = """
You are an expert MySQL administrator. Convert the given natural language request into a valid MySQL query.
The SQL database consists of multiple tables like STUDENT, COLLEGE, FACULTY with their respective columns.
You can create more tables, delete any table, perform JOIN operations as well as use aggregate functions,and many more if the user say so.
Rules:
1. Always use valid table and column names from the schema.
2. If the table exists in the schema file, use its column names.
3. Never assume column names—always refer to the schema.
4. Add LIMIT 100 to SELECT queries unless specified otherwise.
5.when there is "schema" in prompt then it should be used as "describe".
6.strictly provide sql query without any extra text.
7.if query is something like "show student table" use it as "SELECT * FROM student;".
8.show schema means describe the table.
9.table ka schema dikhao means describe the table.
10.for any query of create use create if not exist with the given fields.
11. always take each input as lowercase strictly.
IMPORTANT RULE: if a record is used as a foreign key in other table then delete it from other tables as well

"""


def _build_referenced_by(schema):
    """Build map: table_name -> list of 'other_table.column' that reference it."""
    refs = {}
    for table, cols in schema.items():
        for col, data in cols.items():
            fk = data.get("foreign_key")
            if fk:
                ref_table = fk.split("(")[0].strip() if "(" in fk else fk
                ref_table = ref_table.strip("`")
                if ref_table not in refs:
                    refs[ref_table] = []
                refs[ref_table].append(f"`{table}`.`{col}`")
    return refs


def get_gemini_response(prompt, default_table=None):
    if not _ensure_genai_configured():
        return "AI Error: Unable to generate SQL. Please try again later."
    store_all_table_structures(force_update=True)
    schema = load_schema()
    translated_prompt = translate_to_english(prompt)
    mentioned_tables = [table for table in schema.keys() if table.lower() in translated_prompt.lower()]
    if not mentioned_tables and default_table and default_table != "None" and default_table in schema:
        mentioned_tables = [default_table]
        translated_prompt += f"\n\n[Use the table '{default_table}' for this query unless the user explicitly refers to another table.]"
    if mentioned_tables:
        table_details = "\n".join(
            [f"Table `{table}`: Columns → {', '.join(schema[table].keys())}" for table in mentioned_tables]
        )
        relationship_details = []
        for table in mentioned_tables:
            for col, data in schema[table].items():
                if data.get("foreign_key"):
                    relationship_details.append(f"Column `{col}` in `{table}` links to {data['foreign_key']}")
        referenced_by = _build_referenced_by(schema)
        ref_by_lines = []
        for table in mentioned_tables:
            refs = referenced_by.get(table, [])
            if refs:
                ref_by_lines.append(f"Table `{table}` is referenced by: {', '.join(refs)}")
        translated_prompt += f"\n\nSchema Details:\n{table_details}"
        if relationship_details:
            translated_prompt += "\n\nTable Relationships:\n" + "\n".join(relationship_details)
        if ref_by_lines:
            translated_prompt += "\n\nReferenced by (child tables that must be considered for DELETE/UPDATE on the above):\n" + "\n".join(ref_by_lines)
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content([SQL_PROMPT, translated_prompt])
        sql_query = response.text.strip().replace("```sql", "").replace("```", "").strip()
        return sql_query
    except Exception as e:
        return _format_ai_error(e)


FIX_SQL_PROMPT = """You are an expert MySQL administrator. The following MySQL query failed with an error.
Your task: output a corrected MySQL query that fixes the error. Use only valid table and column names from the schema provided.
Rules:
1. Output only the SQL query, no explanation or markdown.
2. Add LIMIT 100 to SELECT queries unless specified otherwise.
3. Preserve the intent of the original request.
"""


def fix_sql_query(failed_sql, error_message, original_prompt=None, default_table=None):
    """Given a failed SQL and error message, returns a corrected SQL query."""
    if not _ensure_genai_configured():
        return "AI Error: Unable to generate SQL. Please try again later."
    store_all_table_structures(force_update=True)
    schema = load_schema()
    prompt = f"""Error from database: {error_message}

Failed query:
{failed_sql}
"""
    if original_prompt:
        prompt += f"\nOriginal user request: {original_prompt}\n"
    mentioned_tables = [t for t in schema.keys() if t.lower() in prompt.lower()]
    if not mentioned_tables and default_table and default_table != "None" and default_table in schema:
        mentioned_tables = [default_table]
    if mentioned_tables:
        table_details = "\n".join(
            [f"Table `{t}`: Columns → {', '.join(schema[t].keys())}" for t in mentioned_tables]
        )
        relationship_details = []
        for t in mentioned_tables:
            for col, data in schema[t].items():
                if data.get("foreign_key"):
                    relationship_details.append(f"Column `{col}` in `{t}` links to {data['foreign_key']}")
        prompt += f"\n\nSchema:\n{table_details}"
        if relationship_details:
            prompt += "\n\nRelationships:\n" + "\n".join(relationship_details)
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content([FIX_SQL_PROMPT, prompt])
        sql_query = response.text.strip().replace("```sql", "").replace("```", "").strip()
        return sql_query
    except Exception as e:
        return _format_ai_error(e)


def get_sql_explanation(sql_query, target_language="en"):
    """Generate a brief explanation of the SQL query in the given language."""
    if not _ensure_genai_configured():
        return "Error generating explanation. Please try again later."
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(
            f"Provide a brief explanation of this SQL query in 2-3 sentences:\n{sql_query}"
        )
        explanation = response.text.strip()
        if target_language != "en":
            translator = GoogleTranslator(source="auto", target=target_language)
            explanation = translator.translate(explanation)
        return explanation
    except Exception as e:
        return _format_ai_error(e)
