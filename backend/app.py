"""
Flask backend for Query Wizard. Same API as the React frontend expects.
Run from project root: python backend/app.py   OR  cd backend && python app.py
"""
import os
from flask import Flask, request, jsonify
from flask_cors import CORS

from db_config import update_env_credentials
from schema_handler import load_schema, store_all_table_structures
from db_handler import execute_query_api
from ai_generator import get_gemini_response, fix_sql_query, get_sql_explanation

app = Flask(__name__)
CORS(
    app,
    resources={
        r"/api/*": {
            "origins": ["http://localhost:5173", "http://127.0.0.1:5173"],
            "allow_headers": ["Content-Type", "Authorization"],
            "methods": ["GET", "POST", "OPTIONS"],
        }
    },
)


def has_db_credentials():
    p = (os.getenv("DB_PASSWORD") or "").strip()
    n = (os.getenv("DB_NAME") or "").strip()
    return bool(p and n)


@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    db_name = (data.get("db_name") or "").strip()
    db_password = data.get("db_password") or ""
    if not db_name or not db_password:
        return jsonify({"detail": "Database name and password required"}), 400
    try:
        update_env_credentials(db_name, db_password)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"detail": str(e)}), 500


@app.route("/api/check-auth", methods=["GET"])
def check_auth():
    return jsonify({"authenticated": has_db_credentials()})


@app.route("/api/schema", methods=["GET"])
def get_schema():
    if not has_db_credentials():
        return jsonify({"detail": "Not authenticated"}), 401
    try:
        schema = load_schema()
        if not schema:
            store_all_table_structures(force_update=True)
            schema = load_schema()
        return jsonify({"schema": schema, "tables": list(schema.keys())})
    except Exception as e:
        return jsonify({"detail": str(e)}), 500


@app.route("/api/generate-sql", methods=["POST"])
def generate_sql():
    if not has_db_credentials():
        return jsonify({"detail": "Not authenticated"}), 401
    data = request.get_json() or {}
    prompt = (data.get("prompt") or "").strip()
    if not prompt:
        return jsonify({"detail": "Prompt required"}), 400
    try:
        sql = get_gemini_response(prompt, default_table=data.get("default_table"))
        return jsonify({"sql": sql})
    except Exception as e:
        return jsonify({"detail": str(e)}), 500


@app.route("/api/execute", methods=["POST"])
def execute():
    if not has_db_credentials():
        return jsonify({"detail": "Not authenticated"}), 401
    data = request.get_json() or {}
    sql = (data.get("sql") or "").strip()
    if not sql:
        return jsonify({"detail": "SQL required"}), 400
    success, err, results = execute_query_api(sql)
    if not success:
        return jsonify({"success": False, "error": err, "results": None})
    return jsonify({"success": True, "error": None, "results": results})


@app.route("/api/fix-sql", methods=["POST"])
def fix_sql():
    if not has_db_credentials():
        return jsonify({"detail": "Not authenticated"}), 401
    data = request.get_json() or {}
    try:
        sql = fix_sql_query(
            data.get("failed_sql", ""),
            data.get("error_message", ""),
            original_prompt=data.get("original_prompt"),
            default_table=data.get("default_table"),
        )
        return jsonify({"sql": sql})
    except Exception as e:
        return jsonify({"detail": str(e)}), 500


@app.route("/api/explanation", methods=["POST"])
def explanation():
    if not has_db_credentials():
        return jsonify({"detail": "Not authenticated"}), 401
    data = request.get_json() or {}
    try:
        text = get_sql_explanation(
            data.get("sql", ""),
            target_language=data.get("language", "en"),
        )
        return jsonify({"explanation": text})
    except Exception as e:
        return jsonify({"detail": str(e)}), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
