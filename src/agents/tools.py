from langchain.tools import tool
from states import FinanceToolState, SearchToolState, RealTimeToolState, TickerResolverState, FilingToolState
from typing import List
import yfinance as yf
# from ..config import Config


@tool
def filings_tool(state : FilingToolState):
    query = state['query']
    

@tool
def financial_statement_fetcher(state : FinanceToolState):
    """
    This tool helps to fetch different financial statements of a company 
    for a period.
    It can return balance sheets, cashflow statments, income statements, ratios
    
    :param state: It has four keys
    ticker : Ticker of the company.
    start_year : Year from which the data is to be extracted
    end_year : Year till which the data is to be extracted
    type_of_statement : The statement you want to fetch balance sheets, cashflow statements, income_statement or ratios
    :type query: str
    """
    pass


@tool
def real_time_data_tool(state : RealTimeToolState):
    """
    Docstring for real_time_data_tool
    
    :param state: Description
    :type state: RealTimeToolState
    """
    pass


@tool
def ticker_resolver(state : TickerResolverState) -> dict:
    """
    This tools helps to find tickers of different companies using yfinance api.
    
    :param state: List of all the companies whose ticker has to be resolved.
    :type state: TickerResolverState
    :return: Returns a dict of companies and their tickers
    :rtype: dict
    """
    company_names = state.company_names

    company_data = {}

    for com in company_names:
        res = yf.Search(com,max_results = 1).quotes
        company_data[com] = res[0]['symbol']

    return company_data 

if __name__ == "__main__":
    apple = yf.Ticker('aapl')
    

