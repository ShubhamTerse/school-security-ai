# School Security AI

## Setup
1. Create a virtual environment: `python -m venv venv`
2. Activate it: `.\venv\Scripts\activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and fill in the values.

## Run Backend
`uvicorn app.main:app --reload`

## Run Frontend
`streamlit run frontend/app.py`
