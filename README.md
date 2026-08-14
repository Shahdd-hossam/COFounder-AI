# COFounder-AI

COFounder-AI is a React + FastAPI workspace for AI-assisted marketing strategy workflows.

## Implemented Feature Architecture

- Frontend module structure inside `app/src/`
	- `components/common`
	- `components/marketing-plan`
	- `components/market-research`
	- `components/swot`
	- `pages/Home.jsx`
	- `pages/MarketingPlan.jsx`
	- `pages/MarketResearch.jsx`
	- `pages/SWOTAnalysis.jsx`
	- `services/api.js`
- Backend module structure inside `backend/app/`
	- `api/routes/marketing_plan.py`
	- `api/routes/market_research.py`
	- `api/routes/swot.py`
	- `services/marketing_service.py`
	- `services/research_service.py`
	- `services/swot_service.py`
	- `services/ai_service.py`
	- `schemas/marketing.py`
	- `schemas/research.py`
	- `schemas/swot.py`
	- `core/config.py`

## Run Frontend

```bash
cd app
npm install
npm start
```

## Run Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Environment Files

- Copy `app/.env.example` to `app/.env`.
- Copy `backend/.env.example` to `backend/.env`.

## API Endpoints

- `POST /api/v1/marketing-plan`
- `POST /api/v1/market-research`
- `POST /api/v1/swot`
- `GET /health`
