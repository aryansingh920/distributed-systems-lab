# cd services/validator-fastapi
# python -m venv .venv && 
# source .venv/bin/activate
# pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 4001 --reload
