
import os
import logging
import google.generativeai as genai
from schema_handler import load_schema, store_all_table_structures
from deep_translator import GoogleTranslator


GOOGLE_API_KEY="AIzaSyCxm_Hm2u8_76YycigJ3QphshgHpuaDjWc"
genai.configure(api_key=GOOGLE_API_KEY)

logging.basicConfig(level=logging.INFO)
translator = GoogleTranslator(source='auto', target='en')

def translate_to_english(text):
    """
    Translates input text to English while keeping table names intact.
    """
    try:
        return translator.translate(text)
    except Exception as e:
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
"""

def get_gemini_response(prompt, default_table=None):
    store_all_table_structures(force_update=True)  #   Ensure schema is fresh

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

        translated_prompt += f"\n\nSchema Details:\n{table_details}"
        if relationship_details:
            translated_prompt += f"\n\nTable Relationships:\n" + "\n".join(relationship_details)

    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content([SQL_PROMPT, translated_prompt])
        sql_query = response.text.strip().replace("```sql", "").replace("```", "").strip()
        return sql_query
    except Exception as e:
        return f"AI Error: {str(e)}"


FIX_SQL_PROMPT = """You are an expert MySQL administrator. The following MySQL query failed with an error.
Your task: output a corrected MySQL query that fixes the error. Use only valid table and column names from the schema provided.
Rules:
1. Output only the SQL query, no explanation or markdown.
2. Add LIMIT 100 to SELECT queries unless specified otherwise.
3. Preserve the intent of the original request.
"""


def fix_sql_query(failed_sql, error_message, original_prompt=None, default_table=None):
    """Given a failed SQL and error message, returns a corrected SQL query."""
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
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content([FIX_SQL_PROMPT, prompt])
        sql_query = response.text.strip().replace("```sql", "").replace("```", "").strip()
        return sql_query
    except Exception as e:
        return f"AI Error: {str(e)}"
