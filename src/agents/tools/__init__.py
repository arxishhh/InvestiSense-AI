from tools.registry import ToolRegistry
from src.agents.tools.tool_functions import *
from src.agents.tools.states import *

registry = ToolRegistry()

kfilingTool = registry.registerTool(
    func = getKFiling,
    name = "10K Filing Extractor",
    description="""Fetch any section of 10-K filing for given tickers and years.""",
    args_schema=TenKFilingToolState
)

qfilingTool = registry.registerTool(
    func = getQFiling,
    name = "10Q Filing Extractor",
    description="""Fetch any section of 10-Q filing for given tickers and years.""",
    args_schema=TenQFilingToolState
)

balanceSheetTool = registry.registerTool(
    func = getBalanceSheet,
    name = "BalanceSheetExtractor",
    description="Extract required balance sheet metrics for the given tickers and years.",
    args_schema=BalanceSheetToolState
)

incomeStatementTool = registry.registerTool(
    func = getIncomeStatement,
    name = "IncomeStatementExtractor",
    description="Extract required income statement metrics for the given tickers and years.",
    args_schema=IncomeStatementToolState
)

cashFlowTool = registry.registerTool(
    func = getCashFlowStatements,
    name = "CashFlowExtractor",
    description="Extract required cash flow metrics for the given tickers and years.",
    args_schema=CashFlowToolState
)

realTimeTool = registry.registerTool(
    func = realTimeDataFetcher,
    name = "RealTimeDataFetcher",
    description="""Fetch any financial real time data for a given ticker.
    tickers: list of ticker symbols (e.g. ['AAPL', 'GOOG'])
    data_type : list of metrics (e.g. ['price','market_cap','volume'])
    period: period to fetch data for must be one of: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
    data_type_options:
    - 'price','market_cap','volume','pe_ratio','high_low','dividend_yield',
    -'earnings_date'
    """,
    args_schema=RealTimeToolState
)

newsTool = registry.registerTool(
    func = newsFetcher,
    name = "NewsFetcher",
    description="Fetches latest news of the given tickers.",
    args_schema=NewsToolState
)

tickerTool = registry.registerTool(
    func = tickerResolver,
    name = "TickerResolver",
    description="Finds ticker for the given companies.",
    args_schema=TickerResolverState
)

AuditorTools = [tickerTool,kfilingTool,qfilingTool]
FinancerTools = [balanceSheetTool,incomeStatementTool,cashFlowTool]
NewsRoomTools = [tickerTool,newsTool,realTimeTool]





