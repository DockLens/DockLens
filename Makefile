api:
	uvicorn app.main:app --reload --port 8000

client:
	uvicorn agent.main:app --reload --port 8001