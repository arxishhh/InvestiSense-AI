from edgar import *
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from uuid import uuid4
from typing import List,Dict,Any
import logging

load_dotenv()

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n","\n\n\n"],
        chunk_size = 1000,
        chunk_overlap = 400
    )

vector_store = Chroma(
        collection_name = str(uuid4()),
        embedding_function=embeddings
    )

def rag(query: str, context: List):

    try:

        docs = build_documents(context)
        if not docs:
            logging.info("No context provided for RAG")

        vector_store.add_documents(docs)
        retriever = vector_store.as_retriever(
            search_type="mmr",
            search_kwargs={"k": 5}
        )
        retrieved = retriever.invoke(query)

        return [
            {
                **doc.metadata,
                "content": doc.page_content
            }
            for doc in retrieved]

    except Exception as e:
        logging.info(f"Error in RAG: {e}")
    
    return []


def build_documents(context : List):

    docs = []
    for cont in context:
        content = cont.get("content")

        if not content:
            continue

        for chunk in splitter.split_text(content):
            docs.append(
                Document(
                    page_content=chunk,
                    id=str(uuid4()),
                    metadata={k: v for k, v in cont.items() if k != "content"}
                )
            )

    return docs

def format_proofs(proofs : List[Dict[str,Any]]) -> str:

    markdown = ""
    if not proofs:
        markdown = "No Proof Found"
    
    for proof in proofs:
        markdown += f"TICKER : {proof.get('ticker','')} | TIME : {proof.get('time','')} | SOURCE : {proof.get('source','')} | {proof.get('section','')}"
        if type(proof.get('content')) == str:
            markdown += f"\n{proof.get('content')}"
        elif type(proof.get('content')) == dict:
            for key,value in proof.get('content').items():
                markdown += f"\n {key} : {value}\n"
        markdown +='\n'
    
    return markdown

def format_history(history: List[Dict[str,str]]) -> str:
    formatted = ""
    history = history[-10:]

    for message in history:
        role = message.get('role','')
        content = message.get('content','')
        formatted += f"{role.upper()} : {content}\n"

    return formatted



