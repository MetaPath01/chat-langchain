.PHONY: start
start:
	uvicorn main:app --reload --port 10002 

.PHONY: format
format:
	black .
	isort .