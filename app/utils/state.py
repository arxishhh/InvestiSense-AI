from langchain.agents import AgentState
from pydantic import BaseModel,Field
from typing import List,Dict,Literal,Annotated

class SupervisorState(AgentState):
    query : str
    role : str
    response : str = ""
    memory : List[Dict[str,str]] = []

class AgentOutput(BaseModel):
    query : str
    response : str


