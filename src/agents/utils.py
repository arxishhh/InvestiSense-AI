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




def rag(query : str,context : List):

    documents = []
    proofs = []

    for cont in context:
        content = cont.get('content')
        if not content :
            continue
        chunks = splitter.split_text(content)
        for c in chunks:
            documents.append(
                Document(
                    page_content = c,
                    id = str(uuid4()),
                    metadata = {
                        key : value for key,value in cont.items() if key != 'content'
                    }
                )
            )
    try :
        vector_store.add_documents(documents)
        retriever = vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={"k":5})
        retrieved = retriever.invoke(query)
        for ret in retrieved:
            proof = ret.metadata
            proof['content'] = ret.page_content
            proofs.append(proof)
    except Exception as e:
        logging.error(f"Something wrong with Vector DB {str(e)}")

    return proofs

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



