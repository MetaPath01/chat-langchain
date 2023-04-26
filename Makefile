.PHONY: start
start:
	uvicorn main:app --reload --host "" --port 9000 

.PHONY: format
format:
	black .
	isort .
dataset_vector_swft:
	python3 ingest_swft.py