"""Load html from files, clean up, split, ingest into Weaviate."""
import pickle

from langchain.document_loaders import CSVLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.faiss import FAISS

from dotenv import load_dotenv
from pathlib import Path
import sys
import os
import argparse

if getattr(sys, 'frozen', False):
    script_location = Path(sys.executable).parent.resolve()
else:
    script_location = Path(__file__).parent.resolve()
load_dotenv(dotenv_path=script_location / '.env')

parser = argparse.ArgumentParser(description='Ingest data.')
parser.add_argument('-t`', '--text',
                    help="Ingest text data.")
args = parser.parse_args()
text = args.text


def ingest_docs():
    """Get documents from web pages."""
    embeddings = OpenAIEmbeddings(model="gpt-4")
    if os.path.exists(f"{script_location}/vectorstore.pkl"):
        with open("vectorstore.pkl", "rb") as f:
            vectorstore = pickle.load(f)
        n_vectorstore = FAISS.from_texts(texts=[text], embedding=embeddings)
        vectorstore.merge_from(n_vectorstore)
    else:
        vectorstore = FAISS.from_texts(texts=[text], embedding=embeddings)

    # Save vectorstore
    with open("vectorstore.pkl", "wb") as f:
        pickle.dump(vectorstore, f)


if __name__ == "__main__":
    ingest_docs()
