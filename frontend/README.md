# Query Wizard – React frontend

TypeScript + React, with **CSS Modules** for scoped styling. Backend: Flask (Python).

**Structure:** `src/api/` (typed API), `src/types/` (shared types), `src/components/<Name>/` (e.g. `Login.tsx` + `Login.module.css`), `App.tsx`, `main.tsx`, global `index.css`.

## Start the app

**1. Start the Flask backend** (from project root):

```bash
./run_backend.sh
```

Or manually: `cd backend && python app.py`. Runs at **http://127.0.0.1:5000**.

**2. Start the React frontend** (new terminal):

```bash
cd frontend
npm install
npm run dev
```

Opens at **http://localhost:5173**. The app (login/main UI) loads immediately.

**3. Open http://localhost:5173** in your browser. Log in with your DB name and password, then use the app.

## Optional: logo

Images (logo, background) live in `frontend/public/assets/`. Add `logo.png` and `backgroundImage.png` there if needed.
