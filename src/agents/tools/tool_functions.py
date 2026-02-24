from src.agents.states import CashFlowMetric,IncomeStatementMetric,BalanceSheetMetric, TenQSECSection, TenKSECSection
import yfinance as yf
from src.agents.utils import rag
from langchain_community.retrievers import TavilySearchAPIRetriever
from edgar import *
from src.config import Config
import yfinance as yf
import logging
from dotenv import load_dotenv

load_dotenv()

def getKFiling(query : str, tickers : List[str], years : List[str], sections : List[TenKSECSection]):
    set_identity(Config.IDENTITY)
    proofs = []
    message = ""

    for ticker in tickers:
        try :
            company = Company(ticker)
            filings = company.get_filings(form='10-K')

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
                        
                        part,num = section.split("-")
                        item_key = f"part_{part}_item_{num}"
                        content = filing_obj[item_key]
                        if content:
                            proofs.append(
                            {
                                'type':'filing',
                                'ticker' : ticker,
                                'time' : str(f.filing_date),
                                'source' : 'SEC 10-K',
                                'section':section,
                                'content': content
                            })
                            message = f"{message} Fetched {section} of {filing_obj.form} for {ticker} {filing_obj.filing_date}"
                        else:
                            message = f"{message} {section} of {filing_obj.form} not avaliable for {ticker} {filing_obj.filing_date}"
                    
                except Exception as e:
                    logging.warning(f"Error fetching file for {f.accession_no}: {e}")
                    continue
            
        except Exception as e:
            logging.error(f"Failed to fetch data for {ticker} : {e}")
            continue
    
    if proofs:
        proofs = rag(query=query,context=proofs)

    return {
        'message' : message,
        'proofs' : proofs
    }

def getQFiling(query : str, tickers : List[str], years : List[str],sections : List[TenQSECSection]):
    set_identity(Config.IDENTITY)

    proofs = []
    message = ""

    for ticker in tickers:
            
        try :
            company = Company(ticker)
            filings = company.get_filings(form='10-Q')

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

                        if '-' in section:
                            _,num = section.split('-')
                            item_key = f'Part II, Item {num}'

                        else :
                            item_key = f'Part I, Item {section}'

                        content = filing_obj[item_key]
                        proofs.append(
                            {
                                'type':'filing',
                                'ticker' : ticker,
                                'time' : str(f.filing_date),
                                'source' : '10-Q',
                                'section':section,
                                'content': content
                            })
                        message = f"{message} Fetched {section} of 10-Q for {ticker} {filing_obj.filing_date}"

                                                
                except Exception as e:
                    message = f"{message} {section} not avaliable for {ticker} {filing_obj.filing_date}"
                    logging.warning(f"Error fetching file for {f.accession_no}: {e}")
                    continue
            
        except Exception as e:
            logging.error(f"Failed to fetch data for {ticker} : {e}")
            continue
    
    if proofs:
        proofs = rag(query=query,context=proofs)

    return {
        'message' : message,
        'proofs' : proofs
    }
                
                        
def getBalanceSheet(tickers : List[str], years : List[str], values : List[BalanceSheetMetric]):
    proofs = []

    for ticker in tickers:
        try:
            company = yf.Ticker(ticker)
            balance_sheet = company.get_balance_sheet(as_dict = True, freq = 'quarterly')

            for time,stats in balance_sheet.items():
                for year in years:
                    if year in str(time):

                        facts = {}
                        for val in values:
                            key = val.value if hasattr(val, "value") else val
                            facts[key] = stats.get(val, None)
                        
                        proofs.append(
                            {
                                'type':'sheets',
                                'ticker':ticker,
                                'time':str(time),
                                'source':'Balance Sheet',
                                'content': facts
                            }
                        )

        except Exception as e:
           logging.error(f"Cannot fetch balance sheet for {ticker} : {e}")
           continue

    message = f"Fetched {' '.join(values)} Balance Sheet of {' '.join(tickers)} for years : {' '.join(years)}"
    return {
        'message' : message,
        'proofs' : proofs
    }



def getIncomeStatement(tickers : List[str], years : List[str], values : List[IncomeStatementMetric]):
    proofs = []
    for ticker in tickers:
        try:
            company = yf.Ticker(ticker)
            income_stmt = company.get_income_stmt(as_dict = True, freq = 'quarterly')

            for time,stats in income_stmt.items():
                for year in years:
                    if year in str(time):

                        facts = {}
                        for val in values:
                            key = val.value if hasattr(val, "value") else val
                            facts[key] = stats.get(val, None)
                        
                        proofs.append(
                            {
                                'type':'sheets',
                                'ticker':ticker,
                                'time':str(time),
                                'source':'Income Statements',
                                'content': facts
                            }
                        )

        except Exception as e:
           logging.error(f"Cannot fetch income statement for {ticker} : {e}")
           continue
    
    message = f"Fetched {' '.join(values)} Income Statment of {' '.join(tickers)} for years : {' '.join(years)}"
    return {
        'message' : message,
        'proofs' : proofs
    }
    

def getCashFlowStatements(tickers : List[str],years : List[str],values : List[CashFlowMetric]):
    proofs = []

    for ticker in tickers:
        try:
            company = yf.Ticker(ticker)
            cash_flow = company.get_cash_flow(as_dict = True, freq = 'quarterly')

            for time,stats in cash_flow.items():
                for year in years:
                    if year in str(time):

                        facts = {}
                        for val in values:
                            key = val.value if hasattr(val, "value") else val
                            facts[key] = stats.get(val, None)
                        
                        proofs.append(
                            {
                                'type':'sheets',
                                'ticker':ticker,
                                'time':str(time),
                                'source':'Cash Flow',
                                'content': facts
                            }
                        )

        except Exception as e:
           logging.error(f"Cannot fetch cash flow for {ticker} : {e}")
           continue
    
    message = f"Fetched {' '.join(values)} Cash Flow Statement of {' '.join(tickers)} for years : {' '.join(years)}"
    return {
        'message' : message,
        'proofs' : proofs
    }


def realTimeDataFetcher(tickers : List[str],period : str,data_type : List[str]):
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
                        ticker_data[d] = f"Could not fetch {d} for {ticker}. The symbol may be invalid or delisted."
                else:
                    ticker_data[d] = f'Invalid data type: {d}'
            proofs.append(
                {
                    'type':'market_data',
                    'ticker':ticker,
                    'time':period,
                    'source':'YFinance',
                    'content':ticker_data
                }
            )
        except Exception as e:
            logging.warning(f"Ticker {ticker} not found or may be delisted. : {e}")
            continue
    message = f"Fetched Real Time {' '.join(data_type)} for {' '.join(tickers)}"

    return {
        'message':message,
        'proofs':proofs
    }

def newsFetcher(tickers : List[str]):
    tickers = " ".join(tickers)
    proofs = []
    try :
        companies = yf.Tickers(tickers)
        try : 
            news = companies.news()
            if not news:
                return proofs
            
            for ticker,value in news.items():

                company_news = ""
                for i in range(len(value)):
                    company_news = company_news+f"{value[i].get('content').get('title')}\n{value[i].get('content').get('summary')}\n"
                
                proofs.append(
                    {
                        'type':'news',
                        'tickers':ticker,
                        'time':"latest",
                        'source':'YFinance News',
                        'content':company_news
                    }) 
        except Exception as e:
            logging.warning(f"Cannot fetch news for {tickers} : {e}")
    except Exception as e:
        logging.error(f"Error finding {tickers} : {e}")

    message = f"Fetched Latest News For {' '.join(tickers)}"
    return {
        "message" : message,
        "proofs" : proofs
    }

def search(query : str):

    proofs = []
    message = ""
    try :
        retriever = TavilySearchAPIRetriever(k = 10
                                            ,include_domains= ["reuters.com","bloomberg.com","nasdaq.com","marketwatch.com","forbes.com","finance.yahoo.com",
                                                               "barchart.com","cnbc.com","tradersunion.com"]
                                            ,exclude_domains = ["reddit.com","youtube.com","twitter.com","x.com","quora.com","instagram.com","facebook.com"])
        result = retriever.invoke(query)
        for res in result:
            data = res.metadata
            if data.get('score') > 0.85:
                proofs.append({
                    'type':'search',
                'source':data.get('source',""),
                'content':res.page_content})
        message = message+f"Fetched online results for {query}"
    except Exception as e:
        message = f"Failed to search for {query}"
        logging.error(f"{message} : {e}")

    
    return {
        'message':message,
        'proofs':proofs
    }
    
def tickerResolver(company_names : List[str]) -> dict:
    company_data = {}

    for com in company_names:
        try : 
            res = yf.Search(com,max_results = 1).quotes
            company_data[com] = res[0]['symbol']
        except Exception as e:
            logging.error(f"Cannot fetch ticker for {com} : {e}")
            continue
    
    message = f"Fetched Tickers {str(company_data)}"
    return {
        'message': message,
        'proofs' : [company_data]
    }

if __name__ == "__main__":
    print(search(query='company with the highest revenue in 2025'))


    

