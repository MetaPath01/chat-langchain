"""Load html from files, clean up, split, ingest into Weaviate."""
import pickle

from langchain.document_loaders import CSVLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Pinecone

from dotenv import load_dotenv
from pathlib import Path
import sys
import os
import argparse
import pinecone

if getattr(sys, 'frozen', False):
    script_location = Path(sys.executable).parent.resolve()
else:
    script_location = Path(__file__).parent.resolve()
load_dotenv(dotenv_path=script_location / '.env')

parser = argparse.ArgumentParser(description='Ingest data.')
parser.add_argument('-t`', '--text',
                    help="Ingest text data.")
parser.add_argument('-i', '--index_name',
                    help="Index's name")
args = parser.parse_args()
text = args.text
index_name = args.index_name

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENV")
# initialize pinecone
pinecone.init(
    api_key=PINECONE_API_KEY,  # find at app.pinecone.io
    environment=PINECONE_ENV  # next to api key in console
)


def ingest_docs():
    """Get documents from web pages."""
    embeddings = OpenAIEmbeddings(model="gpt-4")
    # db = Pinecone.from_documents(
    #     documents=documents, embedding=embeddings, index_name=index_name)
    db = Pinecone.from_existing_index(index_name, embeddings)
    db.add_texts(texts=[text])
    if db == None:
        print("None")


if __name__ == "__main__":
    ingest_docs()
