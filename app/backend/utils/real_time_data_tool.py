from langchain_core.tools import tool
from typing import List
import os
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
import yfinance as yf
import asyncio

load_dotenv()
model = ChatGroq(model_name = os.getenv('OPENAI_MODEL'))

@tool
def fetch_real_time_data(tickers : List[str], data_type : List[str], period : str = '1d') -> dict:
    """Fetch any financial data for a given ticker.
    tickers: list of ticker symbols (e.g. ['AAPL', 'GOOG'])
    data_type : list of metrics (e.g. ['price','market_cap','volume'])
    period: period to fetch data for must be one of: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
    data_type_options:
    - 'price','market_cap','volume','pe_ratio','high_low','dividend_yield',
    -'earnings_date'
    """
    results = {}
    for t in tickers:
        try:
            stock = yf.Ticker(t)
            try:
                info = stock.info

            except Exception as e:
                results[t] = {"error": f"Information not available."}
            ticker_data = {}
            mapping = {
                'price': lambda: stock.history(period=period)['Close'].iloc[-1],
                'market_cap': lambda: info.get('marketCap'),
                "volume": lambda: info.get('volume'),
                "pe_ratio": lambda: info.get('trailingPE'),
                "high_low": lambda: (info.get('dayHigh'), info.get('dayLow')),
                "dividend_yield": lambda: info.get('dividendYield'),
                "earnings_date": lambda: stock.earnings_dates.head(1).to_dict() if hasattr(stock,'earnings_dates') else None,
            }
            for d in data_type:
                if d in mapping:
                    try:
                        ticker_data[d] = mapping[d]()
                    except Exception:
                        ticker_data[d] = f"Could not fetch {d} for {t}. The symbol may be invalid or delisted."
                else:
                    ticker_data[d] = f'Invalid data type: {d}'
            results[t] = ticker_data
        except Exception as e:
            results[t] = {"error": f"Ticker {t} not found or may be delisted."}
            continue

    return results

llm_with_tools = model.bind_tools([fetch_real_time_data])
async def real_time_query(**kwargs):
    """Perform a real-time query with a given role.

    Args:
        **kwargs: Keyword arguments.
            query (str): The query to be executed.
            role (str): The role of the user.

    Returns:
        str: The result of the real-time query, or an error message if real-time data cannot be fetched.
    """
    query, role = kwargs['query'], kwargs['role']
    messages = [
        HumanMessage(query)
    ]
    result = await llm_with_tools.ainvoke(messages)
    messages.append(result)
    if result.tool_calls:
        call = result.tool_calls[0]
        res = await asyncio.to_thread(fetch_real_time_data.invoke, call)
        messages.append(res)
        prompt = PromptTemplate(
            template='''You are a highly professional {role} in a big finance company.You will be given some data form a good answer from the data and the question
            Data : {data}
            Question : {question}.Round off the data to two decimal places.No preamble.Use proper units.
            ''',
            input_variables=['data', 'question','role']
        )
        parser = StrOutputParser()
        chain = prompt | model | parser
        return await chain.ainvoke({'data': res.content, 'question': query,'role': role})
    else :
        return 'Cannot fetch real time data'


if __name__ == '__main__':
    result = asyncio.run(real_time_query(query = "What is the current stock price of Apple and tell its high and low",role = 'analyst'))
    print(result)




