from typing import TypedDict,Dict,List
from pydantic import BaseModel,Field
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    query : str
    final_response : str
    messages : Dict[BaseMessage]
    #WebSockets
    status : str = Field(default = "intermediate")
    current_process : str
    #Context
    filing_data : str
    financial_data : str
    real_time_data : str
    news : str
    search : str
    #Company Data
    company_and_year= Dict[str, List[str]]

class FinanceToolState(BaseModel):
    company_and_year = Dict[str,List[str]]

class RealTimeToolState(BaseModel):
    pass

class SearchToolState(BaseModel):
    query : str


    



