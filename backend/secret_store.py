import os

try:
    import keyring
except Exception:  # pragma: no cover - dependency/runtime availability
    keyring = None


SERVICE_NAME = "querywizard"
GOOGLE_API_KEY_ITEM = "google_api_key"


def get_google_api_key() -> str:
    """Return API key from env first, then OS keychain."""
    env_key = (os.getenv("GOOGLE_API_KEY") or "").strip()
    if env_key:
        return env_key
    if keyring is None:
        return ""
    try:
        stored = keyring.get_password(SERVICE_NAME, GOOGLE_API_KEY_ITEM) or ""
        return stored.strip()
    except Exception:
        return ""


def set_google_api_key(api_key: str) -> bool:
    """Store API key in OS keychain. Returns True on success."""
    clean = (api_key or "").strip()
    if not clean:
        return False
    os.environ["GOOGLE_API_KEY"] = clean
    if keyring is None:
        return False
    try:
        keyring.set_password(SERVICE_NAME, GOOGLE_API_KEY_ITEM, clean)
        return True
    except Exception:
        return False
