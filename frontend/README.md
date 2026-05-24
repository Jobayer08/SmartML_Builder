# SmartML Frontend

Minimal React + Vite frontend scaffold for SmartML backend.

Quick start

1. Change into frontend:

```bash
cd frontend
```

2. Install dependencies:

```bash
npm install
```

3. Start dev server:

```bash
npm run dev
```

Notes
- The frontend expects the backend at `http://localhost:8000` (adjust `src/api/api.js` if needed).
- Tailwind is preconfigured via `tailwind.config.js` and `src/index.css`.

Files created
- `src/pages/*` — Login, Register, Dashboard, TrainModel, PredictCSV, PredictImage, PredictNC4
- `src/components/*` — Navbar
- `src/api/api.js` — axios wrapper that reads token from `localStorage`

This scaffold is intentionally minimal — extend components and styles as needed.
