from collections import defaultdict
from dotenv import load_dotenv
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.tools import StructuredTool
from app.backend.utils.routing_classifier_filter import filter
import warnings
import os
import asyncio
from pydantic import BaseModel,Field,ConfigDict
load_dotenv()

class RAG(BaseModel):
    query : str

from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore

def rag(query : str):
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    index_name = "investisense-db"
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    pc = Pinecone(api_key=PINECONE_API_KEY)
    index = pc.Index(index_name)
    vector_store = PineconeVectorStore.from_existing_index(
        index_name=index_name,
        embedding=embeddings
    )

    result = filter(query = query)
    question = result['Refined']['query']
    fil = result['Filter']
    for key,entry in fil.items():
        if entry[0] is None:
            return 'Cannot fetch data'
    where = {
        '$and': [
            {'ticker': {'$in': fil['ticker']}},
            {'year': {'$in': fil['year']}},
            {'sec': {'$in': fil['sec']}},
        ]
    }
    retriever = vector_store.as_retriever(search_kwargs={'k': 15, 'filter': where})
    docs = retriever.invoke(question)
    context = structured_result(result = docs)
    return context


def structured_result(**kwargs):
    """Structure result data into a hierarchical dictionary and format as markdown.

    Args:
        **kwargs: Keyword arguments, including 'result' which contains the data to structure.

    Returns:
        str: The structured result data formatted as markdown.
    """
    structured_dict = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    for r in kwargs['result']:
        metadatas = r.metadata
        ticker = metadatas['ticker']
        year = metadatas['year']
        sec = metadatas['sec']
        structured_dict[ticker][year][sec].append(r.page_content)
    return format_markdown(dict = structured_dict)

def format_markdown(**kwargs):
    """Generate markdown text from a given dictionary of ticker symbols, years, and sections.

    Args:
        **kwargs (dict): A dictionary containing 'dict' key with nested structure of ticker symbols, years, and sections.
                         The 'dict' value should be a dictionary where each key is a ticker symbol and each value is another
                         dictionary with year as key and another dictionary as value. The innermost dictionary should have
                         section as key and list of strings as value.

    Returns:
        str: Formatted markdown text.
    """
    markdown = ""
    for ticker,years in kwargs['dict'].items():
        markdown += f"## {ticker}\n"
        for year,sections in years.items():
            markdown += f"### {year}\n"
            for sec,content in sections.items():
                content ='\n'.join(content)
                markdown += f"### {sec}\n{content}\n"
    return markdown

rag_tool = StructuredTool.from_function(
    func = rag,
    name = 'RagTool',
    description = """Retrieve and generate a response based on a query.This tool has access to 10-K filings of different companies and 
    can answer a query which requires textual data.
    Args:
    query (str): The query to be processed.
    Returns:
        str: The generated response to the query.
    """,
    args_schema = RAG
)

if __name__ == '__main__':
    query = "What are the lawsuits filed by Apple in 2022"
    print(rag(query))