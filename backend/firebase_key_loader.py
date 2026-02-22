"""
Fetch GOOGLE_API_KEY (Gemini) from Firebase Realtime Database.
Only this source is used for the API key; .env and secret_store are not used for it.
"""
import json
import logging
import os
import ssl
import urllib.request

try:
    import certifi
except ImportError:
    certifi = None

# Firebase RTDB config (querywizard-8fbb3) - only databaseURL needed for REST
FIREBASE_DATABASE_URL = os.getenv(
    "FIREBASE_DATABASE_URL",
    "https://querywizard-8fbb3-default-rtdb.asia-southeast1.firebasedatabase.app",
).rstrip("/")

# Optional: legacy database secret for auth (Project settings -> Service accounts -> Database secrets)
FIREBASE_DB_SECRET = (os.getenv("FIREBASE_DB_SECRET") or "").strip()

# In-memory cache so we don't hit Firebase on every request
_cached_key = None

logging.basicConfig(level=logging.INFO)


def get_google_api_key() -> str:
    """Return GOOGLE_API_KEY from Firebase Realtime Database. Cached per process."""
    global _cached_key
    if _cached_key is not None:
        return _cached_key
    url = f"{FIREBASE_DATABASE_URL}/GOOGLE_API_KEY.json"
    if FIREBASE_DB_SECRET:
        url += f"?auth={FIREBASE_DB_SECRET}"
    try:
        req = urllib.request.Request(url)
        # Use certifi bundle so SSL verification works on macOS and other systems
        if certifi is not None:
            ctx = ssl.create_default_context(cafile=certifi.where())
        else:
            ctx = ssl.create_default_context()
        with urllib.request.urlopen(req, timeout=10, context=ctx) as resp:
            data = resp.read().decode()
        value = json.loads(data)
        if isinstance(value, str):
            _cached_key = value.strip()
        elif isinstance(value, dict) and "GOOGLE_API_KEY" in value:
            _cached_key = (value["GOOGLE_API_KEY"] or "").strip()
        else:
            _cached_key = ""
        # Debug: remove in production to avoid exposing key in logs
        print("[firebase_key_loader] GOOGLE_API_KEY:", _cached_key or "(empty)")
        return _cached_key or ""
    except Exception as e:
        logging.warning("Firebase RTDB fetch for GOOGLE_API_KEY failed: %s", e)
        return ""
