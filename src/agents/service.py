import requests
from config import Config
from langchain.agents import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts.chat import ChatPromptTemplate
from langgraph.graph import StateGraph,START,END
from src.agents.tools.states import AgentState
import requests
from typing import Dict,List
import requests
from config import Config


def get_prompt(prompt_name : str) -> str:

    user = Config.GITHUB_USER
    repo = Config.PROMPT_REPO
    directory = Config.DIR

    url = f"https://raw.githubusercontent.com/{user}/{repo}/main/{directory}/{prompt_name}.md"
    try : 
        prompt = requests.get(url).text
    except Exception:
        raise RuntimeError("Cannot Fetch The Required Prompt")

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

def intializing_graph() -> StateGraph:

    user = Config.GITHUB_USER
    repo = Config.PROMPT_REPO

    graph = StateGraph()
    url = f"https://raw.githubusercontent.com/{user}/{repo}/main/node_registry.json"

    try : 
        node_registry = requests.get(url).json
    
    except Exception :
        raise RuntimeError("Cannot Fetch Node Registry")

    

    for node_name,node in node_registry.items():
        graph.add_node(node_name,node)
        if node_name == "supervisor":
            graph.add_edge(START,node_name)
        
        if node_name == "replier":
            graph.add_edge(node_name,END)
        
    
    graph.compile()
    return graph

async def collecing_agents(llm : ChatGoogleGenerativeAI) -> dict:

    user = Config.GITHUB_USER
    repo = Config.PROMPT_REPO

    url = f"https://raw.githubusercontent.com/{user}/{repo}/main/agent_registry.json"
    agents = {}
    
    try : 
        agent_registry = requests.get(url).json()
    except Exception:
        raise RuntimeError("Cannot Fetch Agent Registry")
    
    for agent_name,tools in agent_registry.items():
        agent = initialize_agent(llm=llm,tools=tools)
        agents[agent_name] = agent

    return agents













    


    
         

    

    


    
    



    