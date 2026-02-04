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
    filing_data : str
    financial_data : str
    real_time_data : str
    news : str
    search : str
    #Company Data
    company_and_year= Dict[str, List[str]]

class FilingToolState(BaseModel):
    query : str
    ticker : str
    years : List[str]
    sections : List[str]
    
class FinanceToolState(BaseModel):
   ticker : str
   start_year : str
   end_year : str
   type_of_statement : str

class RealTimeToolState(BaseModel):
    pass

class SearchToolState(BaseModel):
    query : str = Field(...,description="The information that we want to get from the internet.")

class TickerResolverState(BaseModel):
    company_names : List[str] = Field(...,description = "This is the list of all the companies whose ticker we want to extract" \
    "to solve the query.")

class PolygonAPIWrapperState(BaseModel):
    pass

    



