from tools.registry import ToolRegistry
from src.agents.tools.tool_functions import *
from src.agents.tools.states import *

registry = ToolRegistry()

filingTool = registry.registerTool(
    func = getFiling,
    name = "Filing Extractor",
    description=" ",
    args_schema=FilingToolState
)

balanceSheetTool = registry.registerTool(
    func = getBalanceSheet,
    name = "BalanceSheetExtractor",
    description="",
    args_schema=FinanceToolState
)

incomeStatementTool = registry.registerTool(
    func = getIncomeStatement,
    name = "IncomeStatementExtractor",
    description="",
    args_schema=FinanceToolState
)

cashFlowTool = registry.registerTool(
    func = getCashFlowStatements,
    name = "CashFlowExtractor",
    description="",
    args_schema=FinanceToolState
)

realTimeTool = registry.registerTool(
    func = realTimeDataFetcher,
    name = "RealTimeDataFetcher",
    description="",
    args_schema=RealTimeToolState
)

newsTool = registry.registerTool(
    func = newsFetcher,
    name = "NewsFetcher",
    description="",
    args_schema=NewsToolState
)

tickerTool = registry.registerTool(
    func = tickerResolver,
    name = "TickerResolver",
    description="",
    args_schema=TickerResolverState
)

AuditorTool = [tickerTool,filingTool,incomeStatementTool,cashFlowTool,balanceSheetTool]
NewsRoomTool = [tickerTool,newsTool,realTimeTool]





