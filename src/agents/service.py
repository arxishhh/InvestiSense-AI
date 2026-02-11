import requests
from langgraph.graph import StateGraph,START,END
from langchain_core.prompts import PromptTemplate
import requests
from typing import Dict,List
import logging
import requests
from src.agents.tools.registry import ToolRegistry
from src.agents.tools.tool_functions import *
from src.agents.states import *
from src.config import Config


def get_prompt(prompt_name : str) -> str:

    user = Config.GITHUB_USER
    repo = Config.PROMPT_REPO
    directory = Config.DIR

    url = f"https://raw.githubusercontent.com/{user}/{repo}/main/{directory}/{prompt_name}.md"
    try : 
        template = requests.get(url).text
    except Exception as e :
        raise logging.error(f"Cannot Fetch The Prompt {prompt_name} : {e}")

    return template

def intializing_graph() -> StateGraph:

    user = Config.GITHUB_USER
    repo = Config.PROMPT_REPO

    graph = StateGraph()
    url = f"https://raw.githubusercontent.com/{user}/{repo}/main/node_registry.json"

    try : 
        node_registry = requests.get(url).json
    
    except Exception as e :
        raise logging.error(f"Cannot Fetch Node Registry : {e}")

    

    for node_name,node in node_registry.items():
        graph.add_node(node_name,node)
        if node_name == "supervisor":
            graph.add_edge(START,node_name)
        
        if node_name == "replier":
            graph.add_edge(node_name,END)
        
    
    graph.compile()
    return graph

def build_tools():
    registry = ToolRegistry()

    kfilingTool = registry.registerTool(
    func_name = getKFiling,
    name = "getKFiling",
    description="""Fetch any section of 10-K filing for given tickers and years.""",
    args_schema=TenKFilingToolState)

    qfilingTool = registry.registerTool(
    func_name = getQFiling,
    name = "getQFiling",
    description="""Fetch any section of 10-Q filing for given tickers and years.""",
    args_schema=TenQFilingToolState)

    balanceSheetTool = registry.registerTool(
    func_name = getBalanceSheet,
    name = "getBalanceSheet",
    description="Extract required balance sheet metrics for the given tickers and years.",
    args_schema=BalanceSheetToolState)

    incomeStatementTool = registry.registerTool(
    func_name = getIncomeStatement,
    name = "getIncomeStatement",
    description="Extract required income statement metrics for the given tickers and years.",
    args_schema=IncomeStatementToolState)

    cashFlowTool = registry.registerTool(
    func_name = getCashFlowStatements,
    name = "getCashFlowStatements",
    description="Extract required cash flow metrics for the given tickers and years.",
    args_schema=CashFlowToolState)

    realTimeTool = registry.registerTool(
    func_name = realTimeDataFetcher,
    name = "realTimeDataFetcher",
    description="""Fetch any financial real time data for a given ticker.
    tickers: list of ticker symbols (e.g. ['AAPL', 'GOOG'])
    data_type : list of metrics (e.g. ['price','market_cap','volume'])
    period: period to fetch data for must be one of: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
    data_type_options:
    - 'price','market_cap','volume','pe_ratio','high_low','dividend_yield',
    -'earnings_date'
    """,
    args_schema=RealTimeToolState)

    newsTool = registry.registerTool(
    func_name = newsFetcher,
    name = "newsFetcher",
    description="Fetches latest news of the given tickers.",
    args_schema=NewsToolState)

    tickerTool = registry.registerTool(
    func_name = tickerResolver,
    name = "tickerResolver",
    description="Finds ticker for the given companies.",
    args_schema=TickerResolverState)

    directory = {
        "AuditorTools" : [tickerTool,kfilingTool,qfilingTool],
        "FinancerTools" : [balanceSheetTool,incomeStatementTool,cashFlowTool],
        "NewsRoomTools" : [tickerTool,newsTool,realTimeTool],
        "AllTools" : registry.getAllTools()
    }

    return directory

def create_auditor_state(query : str):
    template = get_prompt(prompt_name='auditor')
    return {
        'template':template,
        'query':query,
        'done':False,
        'proofs':[],
        'message':""
        }

















    


    
         

    

    


    
    



    