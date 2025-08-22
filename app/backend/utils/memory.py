from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
import os
import asyncio

load_dotenv()
model = ChatGroq(model_name = os.getenv('OPENAI_MODEL'))

async def query_gen_memory(**kwargs):
    """Rephrase a query based on the given text history while preserving context and including relevant details.

    Args:
        **kwargs: Keyword arguments containing the query and memory.
            memory (list): A list of dictionaries containing the text history, where each dictionary has 'User' and 'Message' keys.
            query (str): The query to be rephrased.

    Returns:
        str: The rephrased query.
    """
    memory = kwargs['memory']
    query = kwargs['query']
    history = " "
    for messages in memory:
        history = history + f"{messages['User']}: {messages['Message']} \n"
    prompt = PromptTemplate(
        template = '''From the given history of texts.
        Rephrase the query on the basis of the given text history
        Context Preservation: Query must atleast have company names, dates, and metrics from the context so it can be executed independently.
        Year Inclusion: If the history mentions or implies a year, include it explicitly in the query.make it short.
        Priority should be given to the assistants message while rephrasing the query.
        The reply should only the query. Not a dictionary or JSON file.Priority should be given to the current query.
        If the query is an independent query on its own no need to change it.Give the complete context in a detail way to the query as well.Do not make any information of your own.
        
        History:
        {memory}
        Query:
        {query}
        ''',
        input_variables=['history','query']
    )
    parser = StrOutputParser()
    chain = prompt | model | parser
    query = await chain.ainvoke({'memory':memory,'query':query})
    return query

if __name__ == '__main__':
    memory = [
    {"User": "You", "Message": "What are the management factor of Apple in 2024?"},
    {"User": "Assistant", "Message": '''Hello! Here’s a concise overview of the management‑focused factors Apple highlighted for fiscal 2024:

Macroeconomic environment: Inflation, interest‑rate shifts and currency movements were identified as key external drivers that could materially affect results.
Product and service launch cadence: A steady stream of new offerings powered sales growth, including MacBook Pro (14‑in & 16‑in) and iMac in Q1; MacBook Air (13‑in & 15‑in) in Q2; iPad Air, iPad Pro, major OS updates (iOS 18, macOS Sequoia) and Apple Intelligence™ in Q3; and the iPhone 16 family, Apple Watch Series 10 and AirPods 4 in Q4.
Research & Development: R&D spending rose to $31.37 billion, a 5 % year‑over‑year increase, representing 8 % of net sales. The growth was driven primarily by higher head‑count costs.
Selling, General & Administrative (SG&A): SG&A expenses increased by 
1.2
 
b
i
l
l
i
o
n
t
o
1.2 billionto26.10 billion (5 % YoY), remaining at about 7 % of net sales.
Overall operating expenses: Total operating costs climbed 5 % YoY to $57.47 billion, accounting for 15 % of net sales (up from 14 % in 2023).
Tax provision and effective tax rate: The tax expense surged to $29.75 billion, a 78 % YoY rise, pushing the effective tax rate to 24.1 % (from 14.7 % in 2023).
Geographic performance: Regional sales showed mixed results—Americas grew 3 % to 
167.0
 
b
i
l
l
i
o
n
,
E
u
r
o
p
e
u
p
7
 
167.0 billion,Europeup7 101.3 billion, Greater China declined 8 % to 
66.95
 
b
i
l
l
i
o
n
,
a
n
d
J
a
p
a
n
r
o
s
e
3
 
66.95 billion,andJapanrose3 25.05 billion.
Currency impact: A weaker foreign‑currency environment relative to the U.S. dollar negatively affected Rest of Asia‑Pacific sales.
State‑aid tax obligation: Apple disclosed a pending €14.2 billion (≈ $15.8 billion) payment to Ireland, held in escrow and unavailable for general use.
These factors collectively shaped Apple’s performance and strategic outlook for 2024.'''},
    {"User": "You", "Message": "rate it out of 10"}]
    print(asyncio.run(query_gen_memory(query = 'rate it out of 10',memory = memory)))