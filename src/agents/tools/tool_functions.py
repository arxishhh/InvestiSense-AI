from langchain.tools import tool
from src.agents.tools.states import FinanceToolState, RealTimeToolState, TickerResolverState, FilingToolState, NewsToolState
import yfinance as yf
from src.agents.tools.utils import rag
from edgar import *
from src.config import Config
import yfinance as yf
import logging


async def getFiling(state : FilingToolState):
        
        tickers = state.get('tickers',[])
        years = state.get('years',[])
        query = state.get('query'," ")
        sections = state.get('sections',[])
        form = state.get('form','10-K')

        set_identity(Config.IDENTITY)

        proofs = []

        for ticker in tickers:
            
            try :
                company = Company(ticker)
                filings = company.get_filings(form=form)

                if not filings:
                    continue

                targetted_filings = [
                    f for f in filings
                    if any(year in str(f.filing_date) for year in years)
                ]

                for f in targetted_filings:
                    try :
                        filing_obj = f.obj()
                        if not filing_obj :
                            continue

                        for section in sections:

                            item_key = f"Item {section}"
                            content = obj[item_key]

                            proofs.append(
                                {
                                    'ticker' : ticker,
                                    'time' : str(f.filing_date),
                                    'source' : form,
                                    'section':section,
                                    'content': content
                                })
                    
                    except Exception as e:
                        logging.warning(f"Error fetching file for {f.accession_no}: {e}")
                        continue
            
            except Exception as e:
                logging.error(f"Failed to fetch data for {ticker} : {e}")
                continue

        return rag(query=query,context=proofs)
                
                        
async def getBalanceSheet(state : FinanceToolState):

    tickers = state.get('tickers',[])
    years = state.get('years',[])
    values = state.get('values',[])

    proofs = []

    for ticker in tickers:
        try:
            company = yf.ticker(ticker)
            balance_sheet = company.get_balance_sheet(as_dict = True, freq = 'quarterly')

            for time,stats in balance_sheet.items():
                for year in years:
                    if year in str(time):

                        facts = {}
                        for val in values:
                            facts(val) = stats.get(val,None)
                        
                        proofs.append(
                            {
                                'ticker':ticker,
                                'time':str(time),
                                'source':'Balance Sheet',
                                'content': facts
                            }
                        )

        except Exception as e:
           logging.error(f"Cannot fetch balance sheet for {ticker} : {e}")
           continue
    
    return proofs



async def getIncomeStatement(state : FinanceToolState):

    tickers = state.get('tickers',[])
    years = state.get('years',[])
    values = state.get('values',[])

    proofs = []

    for ticker in tickers:
        try:
            company = yf.ticker(ticker)
            income_stmt = company.get_income_stmt(as_dict = True, freq = 'quarterly')

            for time,stats in income_stmt.items():
                for year in years:
                    if year in str(time):

                        facts = {}
                        for val in values:
                            facts(val) = stats.get(val,None)
                        
                        proofs.append(
                            {
                                'ticker':ticker,
                                'time':str(time),
                                'source':'Income Statements',
                                'content': facts
                            }
                        )

        except Exception as e:
           logging.error(f"Cannot fetch income statement for {ticker} : {e}")
           continue
    
    return proofs
    

async def getCashFlowStatements(state : FinanceToolState):
    
    tickers = state.get('tickers',[])
    years = state.get('years',[])
    values = state.get('values',[])

    proofs = []

    for ticker in tickers:
        try:
            company = yf.ticker(ticker)
            cash_flow = company.get_cash_flow(as_dict = True, freq = 'quarterly')

            for time,stats in cash_flow.items():
                for year in years:
                    if year in str(time):

                        facts = {}
                        for val in values:
                            facts(val) = stats.get(val,None)
                        
                        proofs.append(
                            {
                                'ticker':ticker,
                                'time':str(time),
                                'source':'Cash Flow',
                                'content': facts
                            }
                        )

        except Exception as e:
           logging.error(f"Cannot fetch cash flow for {ticker} : {e}")
           continue
    
    return proofs


async def realTimeDataFetcher(state : RealTimeToolState):

    tickers = state.get('tickers',[])
    period = state.get('period','')
    data_type = state.get('data_type',[])

    proofs = []

    for ticker in tickers:
        try:
            company = yf.Ticker(ticker)
            try:
                info = company.info

            except Exception as e:
                logging.error(f"Information not available for {ticker} : {e}")
            ticker_data = {}
            mapping = {
                'price': lambda: company.history(period=period)['Close'].iloc[-1],
                'market_cap': lambda: info.get('marketCap'),
                "volume": lambda: info.get('volume'),
                "pe_ratio": lambda: info.get('trailingPE'),
                "high_low": lambda: (info.get('dayHigh'), info.get('dayLow')),
                "dividend_yield": lambda: info.get('dividendYield'),
                "earnings_date": lambda: company.earnings_dates.head(1).to_dict() if hasattr(company,'earnings_dates') else None,
            }
            
            for d in data_type:
                if d in mapping:
                    try:
                        ticker_data[d] = mapping[d]()
                    except Exception:
                        ticker_data[d] = f"Could not fetch {d} for {t}. The symbol may be invalid or delisted."
                else:
                    ticker_data[d] = f'Invalid data type: {d}'
            proofs.append(
                {
                    'ticker':ticker,
                    'time':period,
                    'source':'Real Time',
                    'content':ticker_data
                }
            )
        except Exception as e:
            logging.warning(f"Ticker {ticker} not found or may be delisted. : {e}")
            continue

    return proofs

async def newsFetcher(state : NewsToolState):
    tickers = " ".join(state.get("tickers",[]))
    proofs = []
    try :
        companies = yf.Tickers(tickers)
        try : 
            news = companies.news()
            if not news:
                return proofs
            
            for ticker,value in news.items():

                company_news = ""
                for i in range(min(len(value),5)):
                    company_news = company_news+value[i].get('content').get('summary')+'\n'
                
                proofs.append(
                    {
                        'tickers':ticker,
                        'time':"latest",
                        'source':'News',
                        'content':company_news
                    }) 
        except Exception as e:
            logging.warning(f"Cannot fetch news for {tickers} : {e}")
    except Exception as e:
        logging.error(f"Error finding {tickers} : {e}")
    return proofs


async def tickerResolver(state : TickerResolverState) -> dict:
    """
    This tools helps to find tickers of different companies using yfinance api.
    
    :param state: List of all the companies whose ticker has to be resolved.
    :type state: TickerResolverState
    :return: Returns a dict of companies and their tickers
    :rtype: dict
    """
    company_names = state.get('company_names',[])

    company_data = {}

    for com in company_names:
        try : 
            res = yf.Search(com,max_results = 1).quotes
            company_data[com] = res[0]['symbol']
        except Exception as e:
            logging.error(f"Cannot fetch ticker for {com}: {e}")
            continue

    return company_data

if __name__ == "__main__":
    print(getFiling({'tickers':['AAPL'],
                               'years':['2025'],
                               'sections':['1'],
                               'form' : '10-K',
                               'query' : 'What is the business startegy of Apple?'
                               }))

    

