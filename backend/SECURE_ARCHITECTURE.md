# Secure Architecture: Web/Desktop App → Your Backend → Gemini API

## Flow

```
Web / Desktop App  →  YOUR Backend Server  →  Gemini API
     (no API key)        (holds API key)       (Google)
```

1. **App** sends requests to your backend (e.g. `POST /api/generate-sql` with `{ "prompt": "..." }`).
2. **Backend** (Flask) holds `GOOGLE_API_KEY` on the server only. It calls Gemini and returns the result.
3. **API key never leaves the server**; users cannot extract it.

## Setting the API Key on the Server

Set `GOOGLE_API_KEY` in the **server** environment where the backend runs. The app never sends or stores this key.

### Option A: Environment variable (recommended)

When starting the backend:

```bash
export GOOGLE_API_KEY="your-key-from-google-ai-studio"
python backend/app.py
```

Or in systemd, Docker, or your host:

- **systemd**: `Environment="GOOGLE_API_KEY=..."`
- **Docker**: `-e GOOGLE_API_KEY=...` or in `env_file`
- **Host**: Add to `/etc/environment` or your shell profile

### Option B: Server-side .env file

On the server, create a `.env` in the project root (or where the app runs) with:

```
GOOGLE_API_KEY=your-key-here
```

The backend loads this when it starts. **Do not** commit this file; keep it only on the server.

## What the app does NOT do

- Does **not** ask users for a Google API key in the login form.
- Does **not** send the API key from the client to the backend.
- Does **not** bundle or hardcode the key in the desktop app.

## Optional: Extra protection on your backend

You can add:

- **Authentication**: JWT or session after login (you already have DB-based login).
- **Rate limiting**: Limit requests per IP or per user.
- **Usage logging**: Log prompts/responses for abuse detection.
- **Request signing**: Verify requests come from your app.

## Desktop app configuration

Point the desktop or web app to **your backend URL** (e.g. `https://yourdomain.com`). All AI requests go to your server; the key stays on the server.
