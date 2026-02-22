import os
import streamlit as st
import speech_recognition as sr
from db_handler import execute_query
from ai_generator import get_gemini_response, fix_sql_query
from schema_handler import load_schema, store_all_table_structures
from deep_translator import GoogleTranslator
import google.generativeai as genai
from datetime import datetime
import mysql.connector
from db_config import DB_CONFIG, update_env_credentials
import pandas as pd
import base64
import time

# Set page config must be the first Streamlit command
st.set_page_config(
    page_title="Query Wizard",
    layout="wide",
    page_icon="logo.png",
    initial_sidebar_state="expanded"
)

# ----- Login: if not logged in, show only login page (no sidebar) -----
def _has_db_credentials():
    return bool(os.getenv("DB_PASSWORD") and os.getenv("DB_NAME"))

if _has_db_credentials():
    st.session_state["db_logged_in"] = True

if not st.session_state.get("db_logged_in"):
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"] { display: none; }
        [data-testid="stAppViewContainer"] .main .block-container {
            max-width: 420px;
            margin: 0 auto;
            padding: 2.5rem 2rem;
            border: 1px solid #e0e0e0;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            background: #ffffff;
        }
        [data-testid="stAppViewContainer"] .main {
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 2rem;
        }
        .login-title { font-size: 1.75rem; margin-bottom: 0.25rem; font-weight: 600; }
        .login-sub { color: #6c757d; margin-bottom: 1.5rem; font-size: 0.95rem; line-height: 1.4; }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('<h1 class="login-title"> Login Credentials</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="login-sub">Enter your database credentials.</p>',
        unsafe_allow_html=True,
    )
    with st.form("login_form"):
        db_name = st.text_input("Database name", placeholder="e.g. querywizard_db")
        db_password = st.text_input("Database password", type="password", placeholder="Your DB password")
        submitted = st.form_submit_button("Save & continue")
    if submitted:
        if not (db_name and db_password):
            st.warning("Please enter both database name and password.")
        else:
            try:
                update_env_credentials(db_name.strip(), db_password)
                st.session_state["db_logged_in"] = True
                st.success("Credentials saved. Loading app...")
                st.rerun()
            except Exception as e:
                st.error(f"Could not save credentials: {e}")
    st.stop()

schema = load_schema()
if not schema:
    try:
        store_all_table_structures(force_update=True)
        schema = load_schema()
    except Exception:
        pass
tables = list(schema.keys())

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
    }
    .stTextArea>div>div>textarea {
        min-height: 150px;
    }
    .css-1d391kg {
        padding: 1rem;
    }
    .history-item {
        background-color: black;
        color: white;
        padding: 1rem;
        border-radius: 5px;
        margin-bottom: 1rem;
    }
    .language-flag {
        margin-right: 0.5rem;
    }
    .explanation-item {
        background-color: black;
        color: white;
        padding: 1rem;
        border-radius: 5px;
        margin-bottom: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state variables
if "show_details" not in st.session_state:
    st.session_state["show_details"] = False
if "generated_sql" not in st.session_state:
    st.session_state["generated_sql"] = ""
if "user_input" not in st.session_state:
    st.session_state["user_input"] = ""
if "prompt_history" not in st.session_state:
    st.session_state["prompt_history"] = []
if "query_history" not in st.session_state:
    st.session_state["query_history"] = []
if "selected_language" not in st.session_state:
    st.session_state["selected_language"] = "🇺🇸 English"
if "is_loading" not in st.session_state:
    st.session_state["is_loading"] = False
if "query_results" not in st.session_state:
    st.session_state["query_results"] = None
if "last_sql_error" not in st.session_state:
    st.session_state["last_sql_error"] = None

# Language configuration with flags
languages = {
    "🇺🇸 English": "en",
    "🇪🇸 Spanish": "es",
    "🇫🇷 French": "fr",
    "🇩🇪 German": "de",
    "🇮🇳 Hindi": "hi",
    "🇨🇳 Chinese": "zh",
    "🇯🇵 Japanese": "ja",
    "🇷🇺 Russian": "ru"
}

def get_db_username():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SELECT USER()")
        username = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return username
    except Exception as e:
        return "Unknown User"

def translate_prompt(text):
    """
    Translates the user input into English while preserving table names.
    """
    translator = GoogleTranslator(source='auto', target='en')
    try:
        return translator.translate(text)
    except Exception as e:
        st.error(f"Translation Error: {e}")
        return text

def _current_prompt():
    """Current query text (from text area or voice-synced user_input)."""
    return st.session_state.get("user_input", "")

def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("🎙️ Listening... Please speak your query.")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source, timeout=None, phrase_time_limit=None)

    try:
        text = recognizer.recognize_google(audio)
        st.session_state["user_input"] = text
        st.success(f" You said: {text}")
        st.rerun()
    except sr.UnknownValueError:
        st.error(" Could not understand the speech.")
    except sr.RequestError as e:
        st.error(f"Could not request results from Google Speech Recognition service; {e}")

def get_sql_explanation(sql_query, target_language='en'):
    """
    Generates a concise explanation of the SQL query in the specified language.
    """
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        explanation_prompt = f"""
        Provide a brief explanation of this SQL query in 2-3 sentences:
        {sql_query}
        """
        response = model.generate_content(explanation_prompt)
        explanation = response.text.strip()
        
        if target_language != 'en':
            translator = GoogleTranslator(source='auto', target=target_language)
            explanation = translator.translate(explanation)
        
        return explanation
    except Exception as e:
        return f"Error generating explanation: {str(e)}"

st.title("Query Wizard")

# Sidebar configuration
with st.sidebar:
    st.image("logo.png", width="stretch")
    
    # Table selection with improved layout
    st.markdown("### Database Tables")
    selected_table = st.selectbox("Select a Table", ["None"] + list(schema.keys()))
    
    if selected_table and selected_table != "None":
        with st.expander(f" {selected_table} Schema", expanded=False):
            table_columns = schema.get(selected_table, {})
            for col, details in table_columns.items():
                st.markdown(f"🔹 **{col}** : `{details['type']}`")
            
            if st.button(" Display All Records", key="display_all"):
                query = f"SELECT * FROM {selected_table} LIMIT 100;"
                st.session_state["generated_sql"] = query
                execute_query(query)
    
    # Language selection (single select)
    st.markdown("---")
    st.markdown("###  Explanation Language")
    st.session_state["selected_language"] = st.selectbox(
        "Select language for explanation",
        options=list(languages.keys()),
        index=list(languages.keys()).index(st.session_state["selected_language"]) if st.session_state["selected_language"] in languages else 0
    )
    
    # History section with improved layout
    st.markdown("---")
    st.markdown("### Query History")
    
    if st.session_state["prompt_history"]:
        for i, history_item in enumerate(reversed(st.session_state["prompt_history"])):
            with st.expander(f"Query {len(st.session_state['prompt_history']) - i}", expanded=False):
                st.markdown(f"Time: {history_item['timestamp']}")
                st.markdown(f"User: {history_item['username']}")
                st.markdown("---")
                st.markdown("Original Prompt:")
                st.markdown(f'<div class="history-item">{history_item["prompt"]}</div>', unsafe_allow_html=True)
                st.markdown("Generated SQL:")
                st.code(history_item["sql"], language='sql')
    else:
        st.info("No query history yet")

# Main content area
st.markdown("### Enter Your Query")
input_container = st.container()
with input_container:
    # No key= so we can set user_input from voice without Streamlit API error
    user_input = st.text_area(
        "Query Input",
        value=st.session_state.get("user_input", ""),
        height=150,
        label_visibility="collapsed"
    )
    st.session_state["user_input"] = user_input

# First row of buttons
row1_col1, row1_col2 = st.columns([1, 1])
with row1_col1:
    if st.button("Voice Input", key="voice_input"):
        speech_to_text()
with row1_col2:
    if st.button("Generate SQL", key="generate_sql"):
        prompt_text = _current_prompt()
        if prompt_text:
            with st.spinner("Generating SQL query..."):
                translated_input = translate_prompt(prompt_text)
                sql_query = get_gemini_response(translated_input, default_table=selected_table)
                if sql_query:
                    st.session_state["last_sql_error"] = None
                    st.session_state["generated_sql"] = sql_query
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    username = get_db_username()
                    st.session_state["prompt_history"].append({
                        "prompt": prompt_text,
                        "sql": sql_query,
                        "timestamp": current_time,
                        "username": username
                    })
        else:
            st.warning("Please enter a query first.")

# Display generated SQL
if st.session_state.get("generated_sql"):
    st.markdown("### Generated SQL Query")
    st.code(st.session_state["generated_sql"], language='sql')

    # Query explanation with language selection
    with st.expander("Query Explanation", expanded=False):
        lang = st.session_state["selected_language"]
        st.markdown(f"**{lang}:**")
        try:
            explanation = get_sql_explanation(st.session_state["generated_sql"], target_language=languages[lang])
            st.markdown(f'<div class="explanation-item">{explanation}</div>', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error generating {lang} explanation: {str(e)}")
    
    # Execute and Fix buttons
    exec_col, fix_col = st.columns([1, 1])
    with exec_col:
        if st.button("Execute SQL", key="execute_sql"):
            with st.spinner("Executing query..."):
                success, err = execute_query(st.session_state["generated_sql"])
                if not success and err:
                    st.session_state["last_sql_error"] = err
                else:
                    st.session_state["last_sql_error"] = None
    has_error = (
        st.session_state.get("last_sql_error")
        or (st.session_state.get("generated_sql") or "").startswith("AI Error:")
    )
    with fix_col:
        if has_error and st.button("Fix Query", key="fix_sql"):
            with st.spinner("Fixing query..."):
                current_sql = st.session_state["generated_sql"]
                if current_sql.startswith("AI Error:"):
                    error_msg = current_sql
                    current_sql = ""
                else:
                    error_msg = st.session_state.get("last_sql_error") or "Unknown error"
                fixed = fix_sql_query(
                    current_sql,
                    error_msg,
                    original_prompt=_current_prompt(),
                    default_table=selected_table,
                )
                if fixed and not fixed.startswith("AI Error:"):
                    st.session_state["generated_sql"] = fixed
                    st.session_state["last_sql_error"] = None
                    st.success("Query updated. You can execute it again.")
                elif fixed:
                    st.session_state["generated_sql"] = fixed
                st.rerun()

# Add download functionality for query results
if st.session_state.get("query_results") is not None and isinstance(st.session_state["query_results"], pd.DataFrame) and not st.session_state["query_results"].empty:
    st.markdown("###  Download Results")
    csv = st.session_state["query_results"].to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="query_results.csv">📥 Download CSV</a>'
    st.markdown(href, unsafe_allow_html=True)
