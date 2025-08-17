from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
import os
import asyncio

load_dotenv()
model = ChatGroq(model_name = os.getenv('OPENAI_MODEL'))

async def query_gen_memory(query,memory):
    history = " "
    for messages in memory:
        history = history + f"{messages['User']}: {messages['Message']} \n"
    prompt = PromptTemplate(
        template = '''From the given history of texts.
        Rephrase the query on the basis of the given text history
        Context Preservation: Query must atleast have company names, dates, and metrics from the context so it can be executed independently.
        Year Inclusion: If the history mentions or implies a year, include it explicitly in the query.make it short.
        Priority should be given to the assistants message while rephrasing the query.
        The reply should only the query. Not a dictionary or JSON file.
        
        History:
        {history}
        Query:
        {query}
        ''',
        input_variables=['history','query']
    )
    parser = StrOutputParser()
    chain = prompt | model | parser
    query = await chain.ainvoke({'history':history,'query':query})
    return query

if __name__ == '__main__':
    memory = [
    {"User": "You", "Message": "Show me the latest earnings report for Apple."},
    {"User": "Assistant", "Message": "The latest earnings report for Apple shows a revenue of $100B and net income of $25B."},
    {"User": "You", "Message": "What risks are mentioned related to inflation?"},
    {"User": "Assistant", "Message": "The report highlights risks due to rising inflation affecting supply chain costs."}]
    print(asyncio.run(query_gen_memory('How did their revenue trend over the last 4 quarters?',memory)))