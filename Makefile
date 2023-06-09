.PHONY: start
start:
	uvicorn main_pinecone:app --reload --host "" --port 9000 >> ./root.log 2>&1 & 

.PHONY: format
format:
	black .
	isort .
dataset_vector_swft:
	python3 ingest_swft.py
get_twitter_SwftCoin:
	python get_twitter_data.py -u SwftCoin
get_twitter_SWFTBridge:
	python get_twitter_data.py -u SWFTBridge