from dotenv import load_dotenv
from backend.utils.routing_classifier_filter import routing,answer_general_query
from backend.utils.memory import query_gen_memory
from backend.utils.rag_pipeline import rag
from backend.utils.real_time_data_tool import real_time_query
from backend.utils.sql_query_generator import sql_chain
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
import asyncio
import os
import pandas as pd

model = ChatGroq(model_name = os.getenv('OPENAI_MODEL'))
parser_str = StrOutputParser()
pd.set_option('display.max_columns', None)
load_dotenv()
async def buffer():
    return ''
async def context_extractor(query,role):
    splits = routing(query)
    print(splits)
    L = await asyncio.gather(
        answer_general_query(splits['General Query'],role) if len(splits['General Query'])>0 else buffer(),
        rag(splits['Textual Query'],role) if len(splits['Textual Query'])>0 else buffer(),
        real_time_query(splits['Real-Time Query'],role) if len(splits['Real-Time Query'])>0 else buffer(),
        sql_chain(splits['Numerical Query'],role) if len(splits['Numerical Query'])>0 else buffer(),
    )
    text = '\n'.join(L)
    return text

async def answer(query,role,memory):
    query = await query_gen_memory(query,memory)
    context = await context_extractor(query,role)
    if len(context.strip()) == 0:
        context = 'Do not have knowledge about this query'
    prompt = PromptTemplate(
        template='''You are  a professional financial domain expert {role} chatbot name->InvestiSense AI you should sound or reply like your specified given role. You will receive multiple answers or pieces of information related to finance.Your task is to reframe the answer and make them user friendly, ensuring:
Stay within the financial domain – If any part of the input is unrelated to finance, politely state that you can only address finance-related matters and exclude the unrelated parts.
Address salutations – If the user greets you (e.g., “Hi”, “Good morning”), respond politely before providing the combined financial answer.
Clarity & Conciseness – Merge overlapping points, remove redundancy, and keep the tone professional yet approachable.
Logical Flow – Structure your combined answer so it reads naturally, with smooth transitions between ideas.
No extra information – Do not add content not present in the given answers, unless it’s minor phrasing needed for flow.
If the answer say no information available then rephrase it and use that in that in the answer no need to answer things on its own.
No need to user-friendly or something related to it in your reply.You should reply in such a way that you are having a conversation.
Do NOT mention or imply anything about the source or availability of data.  
If some financial data is unavailable, state simply that it is not available or no information was found, without explaining why.  
Avoid phrases like "based on the information you provided" or "the data set contains."  
Focus only on providing the financial insights in a clear, concise, and professional tone.

Input:
Answer: {answer} to be reframed
Use the help of this query {query} to reframe them
Output format:
Return the answer as a proper string suitable for chatbot delivery.
        ''',
        input_variables=['answer','query','role'],
    )
    chain = prompt | model | parser_str
    return await chain.ainvoke({'answer': context,'query':query,'role': role})


if __name__ == '__main__':
    content = "What is Cash Flow Operating"
    print(asyncio.run(answer('Hii','investor',[{'User': 'You', 'Message': 'Hii'}])))