import requests
from config import Config
from langchain.agents import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts.chat import ChatPromptTemplate
from fastapi.responses import JSONResponse
from tools import (rag_tool,real_time_data_tool,search_tool,financial_tool)
from nodes import (supervisor_node,data_extractor_node,analyzer_node,replier_node)
from langgraph.graph import StateGraph


def get_prompt(prompt_name : str) -> str:

    user = Config.GITHUB_USER
    repo = Config.PROMPT_REPO
    directory = Config.DIR

    url = f"https://raw.githubusercontent.com/{user}/{repo}/main/{directory}/{prompt_name}.md"
    prompt = requests.get(url).text

    return prompt


def initialize_agent(agent : str,llm: ChatGoogleGenerativeAI,tools:list):
    prompt = get_prompt(prompt_name = agent)

    system_prompt = ChatPromptTemplate(
        [
            ("system",prompt),
            ("placeholder","{messages}")
        ]
    )

    agent = create_react_agent(
        model = llm,
        tools = tools,
        prompt = system_prompt
    )

    return agent

async def intializing_graph(llm : ChatGoogleGenerativeAI) -> list:

    agents = ["data_extractor","analyzer_agent","replier_agent"] 
    agent_list = []

    for agent in agents:
        tools = []
        if agent == "data_extractor":
            tools = [rag_tool,search_tool,real_time_data_tool,financial_tool]
        agent_list.append(initialize_agent(llm=llm,agent=agent,tools=tools))
         

    

    


    
    



    