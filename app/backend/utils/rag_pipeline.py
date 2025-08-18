from collections import defaultdict
from dotenv import load_dotenv
from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
from langchain_community.embeddings import HuggingFaceEmbeddings
import warnings
import os
from app.backend.utils.routing_classifier_filter import filter,answer_generator
import asyncio
load_dotenv()

warnings.filterwarnings("ignore")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
index_name = "investisense-db"
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(index_name)
vector_store = PineconeVectorStore(index = index,embedding=embeddings)
async def rag(query,role):
    global client
    result = await filter(query)
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
    docs = await retriever.ainvoke(question)
    context = await structured_result(docs)
    return await answer_generator(query,context,role)

async def structured_result(result):
    structured_dict = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    for r in result:
        metadatas = r.metadata
        ticker = metadatas['ticker']
        year = metadatas['year']
        sec = metadatas['sec']
        structured_dict[ticker][year][sec].append(r.page_content)
    return await format_markdown(structured_dict)

async def format_markdown(dict):
    markdown = ""
    for ticker,years in dict.items():
        markdown += f"## {ticker}\n"
        for year,sections in years.items():
            markdown += f"### {year}\n"
            for sec,content in sections.items():
                content ='\n'.join(content)
                markdown += f"### {sec}\n{content}\n"
    return markdown

if __name__ == '__main__':
    query = "What are the lawsuits filed by Apple in 2022"
    print(asyncio.run(rag(query,'analyst')))