import requests
from config import Config
from langchain.agents import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts.chat import ChatPromptTemplate
from langgraph.graph import StateGraph,START,END
from src.agents.tools.states import AgentState
import requests
from typing import Dict,List
import logging
import requests
from config import Config


def get_prompt(prompt_name : str) -> str:

    user = Config.GITHUB_USER
    repo = Config.PROMPT_REPO
    directory = Config.DIR

    url = f"https://raw.githubusercontent.com/{user}/{repo}/main/{directory}/{prompt_name}.md"
    try : 
        prompt = requests.get(url).text
    except Exception as e :
        raise logging.error(f"Cannot Fetch The Prompt {prompt_name} : {e}")

    return prompt

def intializing_graph() -> StateGraph:

    user = Config.GITHUB_USER
    repo = Config.PROMPT_REPO

    graph = StateGraph()
    url = f"https://raw.githubusercontent.com/{user}/{repo}/main/node_registry.json"

    try : 
        node_registry = requests.get(url).json
    
    except Exception as e :
        raise logging.error(f"Cannot Fetch Node Registry : {e}")

    

    for node_name,node in node_registry.items():
        graph.add_node(node_name,node)
        if node_name == "supervisor":
            graph.add_edge(START,node_name)
        
        if node_name == "replier":
            graph.add_edge(node_name,END)
        
    
    graph.compile()
    return graph













    


    
         

    

    


    
    



    