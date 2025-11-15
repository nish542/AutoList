**AutoList**

Simple setup and run instructions for the frontend and backend of this repository.

**Requirements**
- **Python**: Recommended `3.12` (works with `3.11+`).
- **Node.js**: Recommended `18+` (or the version compatible with Vite in `frontend`).
- **npm** (or `pnpm`/`yarn`) for frontend packages.

**Repository layout**
- `backend/` : FastAPI app and Python dependencies
- `frontend/`: Vite + React + TypeScript frontend

**Quickstart (macOS / zsh)**

1) Backend (local development)

- Create and activate a virtual environment (recommended):

```
cd backend
python -m venv venv
source venv/bin/activate
```

- Install Python dependencies:

```
pip install --upgrade pip
pip install -r requirements.txt
```

- Set any required environment variables (example):

```
# Example: export APP_ENV=development
# If your backend requires keys, set them here, e.g.:
# export OPENAI_API_KEY="..."
```

- Run the backend FastAPI server with auto-reload:

```
uvicorn app.main:app --reload --port 8000
```

The backend will be available at `http://localhost:8000` by default.

2) Frontend (local development)

- Install packages and start Vite dev server:

```
cd ../frontend
npm install
npm run dev
```

- The frontend dev server usually runs at `http://localhost:5173` and is configured to proxy API requests (development) to the backend at `http://localhost:8000`.

3) Build for production

- Backend: package or containerize as you prefer (e.g., Docker + Uvicorn/Gunicorn).
- Frontend: build static assets with Vite:

```
cd frontend
npm run build
```

Serve the `dist/` output from your static server or integrate into a deployment flow.

**Notes and recommendations**
- Do NOT commit virtual environments (`venv/`) or large binary packages. This repo includes a `.gitignore` that excludes `venv/` and typical build artifacts.
- If you need PyTorch or other large binaries, install them in the environment rather than committing them to Git. For GPU or CPU-specific wheels, follow the official install instructions from PyTorch.
- If you accidentally committed large files, use `git filter-repo` or Git LFS to remove them; large files (>100 MB) will be rejected by GitHub.

**Troubleshooting**
- If the frontend can't reach the backend, verify both servers are running and that `frontend/vite.config.ts` proxy is enabled in dev mode.
- Confirm environment variables are exported in the same shell session that runs `uvicorn`.
- If you see `ModuleNotFoundError`, ensure your virtualenv is activated and `pip install -r requirements.txt` completed successfully.

**Testing**
- Backend tests (if present) can be run in the `backend/` folder; adjust to your test runner (e.g., `pytest`):

```
cd backend
pytest
```

**Helpful commands summary**

- Start backend:
  - `cd backend && source venv/bin/activate && uvicorn app.main:app --reload --port 8000`
- Start frontend dev server:
  - `cd frontend && npm install && npm run dev`
- Build frontend:
  - `cd frontend && npm run build`

**Want more?**
- I can add API docs, expanded environment-variable lists, Dockerfiles, or step-by-step deployment instructions (Vercel, Netlify, or container registry + cloud VM). Tell me which you'd prefer.

---
Generated on 2025-11-15.
