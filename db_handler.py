import mysql.connector
import streamlit as st
import logging
import re
import pandas as pd
from query_parser import fix_insert_query
from db_config import DB_CONFIG
from schema_handler import store_all_table_structures

logging.basicConfig(level=logging.INFO)

if "query_history" not in st.session_state:
    st.session_state["query_history"] = []

def extract_table_name(query):
    """Extracts the table name from a SQL query. Supports SELECT, INSERT, UPDATE, DELETE, CREATE, JOIN, CURSOR AND PROCEDURES."""
    match = re.search(r"(?:from|into|update|table|join)\s+`?(\w+)`?", query, re.IGNORECASE)
    return match.group(1) if match else None

def execute_query(query):
    """Executes SQL queries, tracks history for undo, and handles errors. Returns (success, error_message)."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
    except mysql.connector.Error as err:
        st.error(f" SQL Execution Error: {err}")
        return (False, str(err))

    queries = query.strip().split(";")
    queries = [q.strip() for q in queries if q.strip()]

    if not queries:
        st.warning("⚠️ No valid SQL query found.")
        return (False, "No valid SQL query found.")

    try:
        for q in queries:
            table_name = extract_table_name(q)

            if not table_name and q.lower().startswith("select"):
                table_name = "Unknown Table"

            st.session_state["query_history"].append(q)

            if q.lower().startswith("insert"):
                corrected_query, values_list = fix_insert_query(q, table_name)
                if not corrected_query:
                    st.error(values_list)
                    return (False, values_list)

                cursor.executemany(corrected_query, values_list)
                conn.commit()
                st.session_state["query_results"] = None
                st.success(f"Insert query executed successfully for `{table_name}`!")

            elif q.lower().startswith("delete"):
                cursor.execute(q)
                conn.commit()
                st.session_state["query_results"] = None
                st.success(f" Delete query executed successfully!")
            
            elif q.lower().startswith("update"):
                cursor.execute(q)
                conn.commit()
                st.session_state["query_results"] = None
                st.success(f" Update query executed successfully!")

            elif q.lower().startswith("show tables"):
                cursor.execute(q)
                results = cursor.fetchall()
                if results:
                    st.write("**Available Tables in Database:**")
                    df = pd.DataFrame({"Tables": [row[0] for row in results]})
                    st.dataframe(df)
                    st.session_state["query_results"] = df
                else:
                    st.warning("No tables found in the database.")
                    st.session_state["query_results"] = None

            elif q.lower().startswith(("select", "show", "describe")):
                cursor.execute(q)
                results = cursor.fetchall()
                column_names = [desc[0] for desc in cursor.description] if cursor.description else []

                if results:
                    st.write(f"**Query Results for `{table_name}`:**")
                    df = pd.DataFrame({col: [row[i] for row in results] for i, col in enumerate(column_names)})
                    st.dataframe(df)
                    st.session_state["query_results"] = df
                else:
                    st.warning(f"No records found in `{table_name}`.")
                    st.session_state["query_results"] = None

            else:
                cursor.execute(q)
                conn.commit()
                st.success(f" Query executed successfully!")

        return (True, None)
    except mysql.connector.Error as err:
        st.error(f" SQL Execution Error: {err}")
        logging.error(f"SQL Execution Error: {err}")
        return (False, str(err))
    finally:
        try:
            while cursor.nextset():
                pass
        except mysql.connector.InterfaceError:
            pass
        try:
            cursor.close()
            conn.close()
        except Exception:
            pass
