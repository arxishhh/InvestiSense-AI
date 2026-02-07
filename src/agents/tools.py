from langchain.tools import tool
from states import FinanceToolState, RealTimeToolState, TickerResolverState, FilingToolState
import yfinance as yf
from src.agents.utils import rag
from edgar import *
from src.config import Config
import yfinance as yf

@tool
def getFiling(state : FilingToolState):
        
        tickers = state['tickers']
        years = state['years']
        query = state['query']
        sections = state['sections']
        form = state['form']

        set_identity(Config.IDENTITY)
        
        company = Company(ticker)
        filings = company.get_filings(form=form)
        context = []
        for ticker in tickers:
            company = Company(ticker)
            filings = company.get_filings(form=form)
            for f in filings:
                for year in years:
                    if year in str(f.filing_date):
                        for section in sections:
                            context.append(
                                {
                                    'ticker':ticker,
                                    'year': year,
                                    'form' : form,
                                    'section' : f'Item {section}',
                                    'content' : f.obj()[f'Item {section}']
                                }
                            )

        if form == '8-K':
            return context
        return rag(query=query,context=context)
    

@tool
def financial_statement_fetcher(state : FinanceToolState):
    """
    This tool helps to fetch different financial statements of a company 
    for a period.
    It can return balance sheets, cashflow statments, income statements, ratios
    
    :param state: It has four keys
    ticker : Ticker of the company.
    years : Years for which you want to find the data
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

    

