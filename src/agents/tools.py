from langchain.tools import tool
from schemas import FinancialToolState, SearchToolState, RealTimeToolState
from typing import List

@tool
def rag_tool(state : FinancialToolState):
    pass

@tool
def financial_tool(state : FinancialToolState):
    pass

@tool
def real_time_data_tool(state : RealTimeToolState):
    pass

@tool
def search_tool(state : SearchToolState):
    pass

@tool
def ticker_resolver(company_names : List[str]):
    return search_tool()
