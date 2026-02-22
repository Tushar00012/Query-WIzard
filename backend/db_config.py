import os
import logging
import re
import sys
from dotenv import load_dotenv

# Project root (parent of backend/)
_DEV_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_APP_DIR = os.path.join(os.path.expanduser("~"), ".querywizard")

if getattr(sys, "frozen", False):
    os.makedirs(_APP_DIR, exist_ok=True)
    _ROOT = _APP_DIR
else:
    _ROOT = _DEV_ROOT


def _candidate_env_paths():
    paths = [os.path.join(_ROOT, ".env")]
    if getattr(sys, "frozen", False):
        paths.append(os.path.join(os.path.dirname(sys.executable), ".env"))
        paths.append(os.path.join(os.getcwd(), ".env"))
    return paths


def _load_env_files(override=False):
    for path in _candidate_env_paths():
        if os.path.isfile(path):
            load_dotenv(path, override=override)


_load_env_files(override=False)

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
    """Path to .env file (project root in dev, user dir in packaged mode)."""
    return os.path.join(_ROOT, ".env")


def refresh_db_config():
    """Reload env and update DB_CONFIG in place so all importers see new values."""
    _load_env_files(override=True)
    global DB_CONFIG
    DB_CONFIG["host"] = os.getenv("DB_HOST", "localhost")
    DB_CONFIG["user"] = os.getenv("DB_USER", "root")
    DB_CONFIG["password"] = os.getenv("DB_PASSWORD", "")
    DB_CONFIG["database"] = os.getenv("DB_NAME", "")


def update_env_credentials(db_name: str, db_password: str) -> None:
    """Write DB credentials to .env and refresh DB_CONFIG. API key is never stored from client."""
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
        elif re.match(r"^\s*GOOGLE_API_KEY\s*=", line):
            new_lines.append(line)
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
