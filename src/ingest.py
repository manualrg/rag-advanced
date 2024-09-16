from pathlib import Path
from uuid import uuid4

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores.chroma import Chroma
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders.directory import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
import os

from langchain_community.document_loaders import PyPDFLoader

from src.mle import utils as mle_utils


def run(file, embeddings, index_name):
    filename = mle_utils.path_data_raw / file
    path_db = mle_utils.path_data_interm / "chroma_langchain_db"
    path_db.mkdir(exist_ok=True, parents=True)

    loader = PyPDFLoader(filename)

    docs = loader.load()

    vector_store = Chroma(
        collection_name=index_name,
        embedding_function=embeddings,
        persist_directory=path_db,
    )

    #uuids = [str(uuid4()) for _ in range(len(docs))]
    uuids = [i for i in range(len(docs))]

    vector_store.add_documents(documents=docs, ids=uuids)

    return vector_store

if __name__ == "__main__":

    load_dotenv()

    embeddings = OpenAIEmbeddings("text-embedding-3-small")
    file = "AIACT_20241689_ES_TXT"
    index_name="ai_act"
    vector_store = run(file, embeddings, index_name)

    retriever = vector_store.as_retriever(
        search_type="mmr", search_kwargs={"k": 1, "fetch_k": 5}
        )
    retriever.invoke("Stealing from the bank is a crime", filter={"source": "news"})

