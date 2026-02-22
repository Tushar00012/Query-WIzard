# Firebase Realtime Database – GOOGLE_API_KEY

The backend loads the **Gemini API key** only from **Firebase Realtime Database**. Other sources (`.env`, login form, keychain) are not used for the API key.

## Setup

1. In [Firebase Console](https://console.firebase.google.com) → your project **querywizard-8fbb3** → **Realtime Database**.
2. At the **root** of the database, add a key named **`GOOGLE_API_KEY`** with the value set to your Gemini API key (e.g. from [Google AI Studio](https://aistudio.google.com/apikey)).

Example structure:

```json
{
  "GOOGLE_API_KEY": "AIzaSy..."
}
```

3. (Optional) For private databases, set **FIREBASE_DB_SECRET** in your server environment. You can create a secret in: Project settings → Service accounts → **Database secrets** (Legacy). Then the backend will use `?auth=<secret>` when reading.

## Backend config

- **FIREBASE_DATABASE_URL** (optional): Defaults to  
  `https://querywizard-8fbb3-default-rtdb.asia-southeast1.firebasedatabase.app`
- **FIREBASE_DB_SECRET** (optional): Legacy database secret for authenticated read.

The key is cached in memory after the first successful fetch.
