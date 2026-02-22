"""
Flask backend for Query Wizard.
Run from project root: python backend/app.py
"""
import os
import sys
from functools import wraps
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

try:
    from .db_config import update_env_credentials, clear_credentials
    from .schema_handler import load_schema, store_all_table_structures, delete_schema_file
    from .db_handler import execute_query_api
    from .ai_generator import get_gemini_response, fix_sql_query, get_sql_explanation, has_api_key
    from .secret_store import set_google_api_key
except ImportError:
    from db_config import update_env_credentials, clear_credentials
    from schema_handler import load_schema, store_all_table_structures, delete_schema_file
    from db_handler import execute_query_api
    from ai_generator import get_gemini_response, fix_sql_query, get_sql_explanation, has_api_key
    from secret_store import set_google_api_key


def has_db_credentials():
    p = (os.getenv("DB_PASSWORD") or "").strip()
    n = (os.getenv("DB_NAME") or "").strip()
    return bool(p and n)


def has_google_api_key():
    return has_api_key()


def has_app_credentials():
    return has_db_credentials()


def json_body():
    return request.get_json(silent=True) or {}


def error(message, status=400):
    return jsonify({"detail": message}), status


def require_auth(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not has_db_credentials():
            return error("Not authenticated", 401)
        return fn(*args, **kwargs)

    return wrapper


def _default_static_dir():
    env_dir = os.getenv("APP_STATIC_DIR", "").strip()
    if env_dir:
        return env_dir
    if getattr(sys, "frozen", False):
        meipass = getattr(sys, "_MEIPASS", "")
        if meipass:
            return os.path.join(meipass, "frontend", "dist")
    return str(Path(__file__).resolve().parents[1] / "frontend" / "dist")


def create_app():
    static_dir = _default_static_dir()
    static_folder = static_dir if os.path.isdir(static_dir) else None

    app = Flask(__name__, static_folder=static_folder, static_url_path="")
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

    @app.route("/api/login", methods=["POST"])
    def login():
        data = json_body()
        db_name = (data.get("db_name") or "").strip()
        db_password = data.get("db_password") or ""
        google_api_key = (data.get("google_api_key") or "").strip()
        if not db_name or not db_password:
            return error("Database name and password required")
        if not google_api_key and not has_google_api_key():
            return error("Google API key required")
        try:
            update_env_credentials(db_name, db_password)
            if google_api_key and not set_google_api_key(google_api_key):
                return error("Could not securely store API key on this machine")
            delete_schema_file()
            return jsonify({"success": True})
        except Exception as e:
            return error(str(e), 500)

    @app.route("/api/check-auth", methods=["GET"])
    def check_auth():
        return jsonify(
            {
                "authenticated": has_app_credentials(),
                "has_db_credentials": has_db_credentials(),
                "has_google_api_key": has_google_api_key(),
            }
        )

    @app.route("/api/logout", methods=["POST"])
    def logout():
        try:
            clear_credentials()
            delete_schema_file()
            return jsonify({"success": True})
        except Exception as e:
            return error(str(e), 500)

    @app.route("/api/schema", methods=["GET"])
    @require_auth
    def get_schema():
        try:
            schema = load_schema()
            if not schema:
                store_all_table_structures(force_update=True)
                schema = load_schema()
            return jsonify({"schema": schema, "tables": list(schema.keys())})
        except Exception as e:
            return error(str(e), 500)

    @app.route("/api/generate-sql", methods=["POST"])
    @require_auth
    def generate_sql():
        data = json_body()
        prompt = (data.get("prompt") or "").strip()
        if not prompt:
            return error("Prompt required")
        try:
            sql = get_gemini_response(prompt, default_table=data.get("default_table"))
            return jsonify({"sql": sql})
        except Exception as e:
            return error(str(e), 500)

    @app.route("/api/execute", methods=["POST"])
    @require_auth
    def execute():
        data = json_body()
        sql = (data.get("sql") or "").strip()
        if not sql:
            return error("SQL required")
        success, err, results = execute_query_api(sql)
        if not success:
            return jsonify({"success": False, "error": err, "results": None})
        return jsonify({"success": True, "error": None, "results": results})

    @app.route("/api/fix-sql", methods=["POST"])
    @require_auth
    def fix_sql():
        data = json_body()
        try:
            sql = fix_sql_query(
                data.get("failed_sql", ""),
                data.get("error_message", ""),
                original_prompt=data.get("original_prompt"),
                default_table=data.get("default_table"),
            )
            return jsonify({"sql": sql})
        except Exception as e:
            return error(str(e), 500)

    @app.route("/api/explanation", methods=["POST"])
    @require_auth
    def explanation():
        data = json_body()
        try:
            text = get_sql_explanation(
                data.get("sql", ""),
                target_language=data.get("language", "en"),
            )
            return jsonify({"explanation": text})
        except Exception as e:
            return error(str(e), 500)

    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def serve_spa(path):
        if path.startswith("api/"):
            return error("API endpoint not found", 404)
        if not app.static_folder:
            return error("Frontend build not found. Build frontend first.", 404)
        full_path = os.path.join(app.static_folder, path)
        if path and os.path.exists(full_path):
            return send_from_directory(app.static_folder, path)
        return send_from_directory(app.static_folder, "index.html")

    return app


app = create_app()


if __name__ == "__main__":
    app.run(
        host=os.getenv("APP_HOST", "127.0.0.1"),
        port=int(os.getenv("APP_PORT", "5000")),
        debug=os.getenv("FLASK_DEBUG", "0") == "1",
    )
