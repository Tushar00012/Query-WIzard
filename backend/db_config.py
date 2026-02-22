import os
import logging
import re
from dotenv import load_dotenv

# Project root (parent of backend/)
_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
load_dotenv(os.path.join(_ROOT, ".env"))

required_vars = ["DB_HOST", "DB_USER", "DB_PASSWORD", "DB_NAME"]
for var in required_vars:
    if not os.getenv(var):
        logging.warning(f"Missing environment variable: {var}")

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", ""),
}


def _env_path():
    """Path to .env file (project root)."""
    return os.path.join(_ROOT, ".env")


def refresh_db_config():
    """Reload env and update DB_CONFIG in place so all importers see new values."""
    load_dotenv(os.path.join(_ROOT, ".env"), override=True)
    global DB_CONFIG
    DB_CONFIG["host"] = os.getenv("DB_HOST", "localhost")
    DB_CONFIG["user"] = os.getenv("DB_USER", "root")
    DB_CONFIG["password"] = os.getenv("DB_PASSWORD", "")
    DB_CONFIG["database"] = os.getenv("DB_NAME", "")


def update_env_credentials(db_name: str, db_password: str) -> None:
    """Write DB_NAME and DB_PASSWORD to .env and refresh DB_CONFIG."""
    path = _env_path()
    lines = []
    if os.path.isfile(path):
        with open(path, "r") as f:
            lines = f.readlines()
    seen = {"DB_NAME": False, "DB_PASSWORD": False}
    new_lines = []
    for line in lines:
        if re.match(r"^\s*DB_NAME\s*=", line):
            new_lines.append(f'DB_NAME="{db_name}"\n')
            seen["DB_NAME"] = True
        elif re.match(r"^\s*DB_PASSWORD\s*=", line):
            new_lines.append(f'DB_PASSWORD="{db_password}"\n')
            seen["DB_PASSWORD"] = True
        else:
            new_lines.append(line)
    if not seen["DB_NAME"]:
        new_lines.append(f'DB_NAME="{db_name}"\n')
    if not seen["DB_PASSWORD"]:
        new_lines.append(f'DB_PASSWORD="{db_password}"\n')
    with open(path, "w") as f:
        f.writelines(new_lines)
    os.environ["DB_NAME"] = db_name
    os.environ["DB_PASSWORD"] = db_password
    refresh_db_config()
