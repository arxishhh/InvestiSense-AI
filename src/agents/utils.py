from edgar import *
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from src.config import Config
from uuid import uuid4
from typing import List,Dict,Any


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
        chunks = splitter.split_text(cont.get('content'))
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

    vector_store.add_documents(documents)
    retriever = vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={"k":5}
    )

    retrieved = retriever.invoke(query)

    for ret in retrieved:
        proof = ret.metadata
        proof['content'] = ret.page_content
        proofs.append(proof)

    return proofs

def format_proofs(proofs : List[Dict[str,Any]]) -> str:

    markdown = ""
    for proof in proofs:
        markdown += f"###{proof.get('ticker')} | ###{proof.get('time')} | ###{proof.get('source')} | ###{proof.get('section','')}"
        if type(proof.get('content')) == list:
            markdown += f"\n{proof.get('content')}"
        else:
            for key,value in proof.get('content'):
                markdown += f"\n###{key} : {value}\n"
        markdown +='\n'
    
    return markdown

def create_auditor_state(query : str):
    return {'query':query,
            'done':False,
            'iterations':0
            }
