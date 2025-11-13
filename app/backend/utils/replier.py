from dotenv import load_dotenv
from app.backend.utils.memory import query_gen_memory
from langchain_core.prompts import PromptTemplate
from app.backend.utils.error_handling import  safe_fallback
from langchain_core.output_parsers import StrOutputParser
from app.utils.state import SupervisorState
from app.agents.supervisor import calling_supervisor_agent
from langchain_groq import ChatGroq
import os
import pandas as pd

model = ChatGroq(model_name = os.getenv('OPENAI_MODEL'))
parser_str = StrOutputParser()
pd.set_option('display.max_columns', None)
load_dotenv()

def answer(state : SupervisorState):
    """Generate a professional and user-friendly financial answer based on the provided query and context.

    Args:
        **kwargs: Keyword arguments containing:
            query (str): The user's query.
            memory (object): Additional memory or context for the query.
            role (str): The role of the chatbot, influencing its tone and response.

    Returns:
        str: A refined and professional financial answer, suitable for chatbot delivery.
    """
    query = state['query']
    memory = state['memory']
    role = state['role']
    state = safe_fallback(query_gen_memory,state = state)
    state = safe_fallback(calling_supervisor_agent,state = state)
    # prompt = PromptTemplate(
    #     template='''You are  a professional financial domain expert {role} chatbot name->InvestiSense AI you should sound or reply like your specified given role. You will receive multiple answers or pieces of information related to finance.Your task is to reframe the answer and make them user friendly, ensuring:
    #     Stay within the financial domain – If any part of the input is unrelated to finance, politely state that you can only address finance-related matters and exclude the unrelated parts.
    #     Address salutations – If the user greets you (e.g., “Hi”, “Good morning”), respond politely before providing the combined financial answer.
    #     Clarity & Conciseness – Merge overlapping points, remove redundancy, and keep the tone professional yet approachable.
    #     Logical Flow – Structure your combined answer so it reads naturally, with smooth transitions between ideas.
    #     No extra information – Do not add content not present in the given answers, unless it’s minor phrasing needed for flow.
    #     If the answer say no information available then rephrase it and use that in that in the answer no need to answer things on its own.
    #     No need to user-friendly or something related to it in your reply.You should reply in such a way that you are having a conversation.
    #     Do NOT mention or imply anything about the source or availability of data.
    #     If some financial data is unavailable, state simply that it is not available or no information was found, without explaining why.
    #     Avoid phrases like "based on the information you provided" or "the data set contains."
    #     Focus only on providing the financial insights in a clear, concise, and professional tone.
    #     Input:
    #     Answer: {answer} to be reframed
    #     Use the help of this query {query} to reframe them
    #     Output format:
    #     Return the answer as a proper string suitable for chatbot delivery.
    #     ''',
    #     input_variables=['answer','query','role'],
    # )
    # chain = prompt | model | parser_str
    # res = chain.invoke({'answer': state['response'],'query':state['query'],'role': state['role']})
    # state['response'] = res
    return state

if __name__ == '__main__':
    content = "What is the current stock price of Apple?"
    memory = [{'User': 'You', 'Message': content}]
    state = SupervisorState(
        query = content,
        role = 'analyst',
        memory = memory
    )
    print(safe_fallback(answer,state = state))