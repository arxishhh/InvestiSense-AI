from typing import TypedDict,Dict,List
from pydantic import BaseModel,Field
from langchain_core.messages import BaseMessage
from uuid import UUID

class AgentState(TypedDict):
    session_id : UUID = Field(default = UUID)

    query : str
    final_response : str
    messages : List[BaseMessage]
    #WebSockets
    status : str = Field(default = "intermediate")
    current_process : str
    #Context
    proofs : List[Dict[str,str]]

class FilingToolState(BaseModel):
    query : str
    tickers : List[str]
    form : str
    years : List[str]
    sections : List[str]
    
class FinanceToolState(BaseModel):
   tickers : List[str]
   years : List[str]
   values : List[str]

class RealTimeToolState(BaseModel):
    tickers : List[str] 
    period : str
    data_type : List[str]

class SearchToolState(BaseModel):
    query : str = Field(...,description="The information that we want to get from the internet.")

class TickerResolverState(BaseModel):
    company_names : List[str] = Field(...,description = "This is the list of all the companies whose ticker we want to extract" \
    "to solve the query.")

class NewsToolState(BaseModel):
    tickers : List[str]


    



