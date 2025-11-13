from app.tools.rag import rag_tool
from app.tools.query_generator import sql_tool
from app.tools.realtime_data_fetcher import fetch_tool
from app.utils.state import SupervisorState,AgentOutput
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    google_api_key=os.getenv('GEMINI_API_KEY')
)
supervisor_agent = create_agent(
    model,
    tools = [rag_tool,sql_tool,fetch_tool],
    system_prompt = "You are a financial assistant chatbot named InvestiSense AI.Use only the information provided by the tools",
    state_schema = SupervisorState,
    response_format = AgentOutput
)
def calling_supervisor_agent(**kwargs) -> SupervisorState:
    state = kwargs['state']
    state['messages'] = [{'role':'user','content':state['query']}]
    role = state.get('role')
    config = {
        "configurable":{
            "role":role
        }
    }
    res = supervisor_agent.invoke(state,config = config)
    state['response'] = res.get('structured_response').response
    return state


if __name__ == '__main__':
    state = SupervisorState(
        messages = [{'role':'user','content': 'Hi'}],
        query = 'Hi',
        role = 'analyst'
    )
    print(calling_supervisor_agent(state = state))

