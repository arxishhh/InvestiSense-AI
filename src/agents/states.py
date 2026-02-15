from typing import TypedDict,Dict,List,Any
from pydantic import BaseModel,Field
from langchain_core.messages import BaseMessage
from uuid import UUID
from enum import Enum

class AgentState(TypedDict):
    session_id : UUID = Field(default = UUID)
    query : str
    final_response : str
    #WebSockets
    #Context
    proofs : List[Dict[str,str]]
    formatted_proofs : str
    analysis : str = " "
    status_messages : str = " "

class Routes(str, Enum):
    AUDITOR = "auditor"
    FINANCER = "financer"
    NEWSROOM ="newsroom"
    ANALYSER = "analyser"
    REPLIER = "replier"

class SupervisorState(BaseModel):
    route : List[Routes] = Field(...,
        description="""
        "auditor" : "Collects financial evidence from SEC filings (10-K, 10-Q) by identifying tickers, years, and required filing sections using tool-based retrieval.",
        "financer" : "Retrieves financial statements (balance sheet, income statement, cash flow) and structured financial data for the requested tickers and years.",
        "newsroom" : "Collects recent financial news, search-based context, and real-time stock data relevant to the query.",
        "analyser" : "Analyzes collected financial, filing, and news evidence to produce a grounded explanation based only on retrieved proofs.",
        "replier" : "Converts the analyzer’s grounded explanation into a clear, user-facing financial response."
        """
    )



class TenKSECSection(str, Enum):
    BUSINESS = "i-1"             
    RISK_FACTORS = "i-1a"        
    UNRESOLVED_STAFF_COMMENTS = "i-1b"
    PROPERTIES = "i-2"           
    LEGAL_PROCEEDINGS = "i-3" 
    MINE_SAFETY = "i-4"
    MARKET_FOR_EQUITY = "ii-5"     
    RESERVED_6 = "ii-6"          
    MDA = "ii-7"                  
    MARKET_RISK = "ii-7a"         
    ACCOUNTING_DISPUTES = "ii-9"   
    INTERNAL_CONTROLS = "ii-9a"    
    OTHER_INFO = "ii-9b"              
    DIRECTORS_GOVERNANCE = "iii-10" 
    EXECUTIVE_COMP = "iii-11"     
    SECURITY_OWNERSHIP = "iii-12"  
    CERTAIN_RELATIONSHIPS = "iii-13"
    AUDIT_FEES = "iii-14"         
    EXHIBITS = "iv-15"


class TenQSECSection(str, Enum):
    FINANCIAL_STATEMENTS = "1"     
    MDA = "2"                    
    MARKET_RISK = "3"             
    CONTROLS_PROCEDURES = "4"      
    LEGAL_PROCEEDINGS = "2-1"        
    RISK_FACTORS = "2-1A"            
    UNREGISTERED_SECURITIES = "2-2"  
    DEFAULTS = "2-3"                 
    MINE_SAFETY = "2-4"             
    OTHER_INFORMATION = "2-5"        
    EXHIBITS = "2-6"    

class BalanceSheetMetric(str, Enum):
    CASH_AND_EQUIVALENTS = "CashAndCashEquivalents"
    ACCOUNTS_RECEIVABLE = "AccountsReceivable"
    INVENTORY = "Inventory"
    TOTAL_CURRENT_ASSETS = "CurrentAssets"
    NET_PPE = "NetPPE"
    TOTAL_ASSETS = "TotalAssets"
    ACCOUNTS_PAYABLE = "AccountsPayable"
    CURRENT_DEBT = "CurrentDebt"
    TOTAL_CURRENT_LIABILITIES = "CurrentLiabilities"
    LONG_TERM_DEBT = "LongTermDebt"
    TOTAL_LIABILITIES = "TotalLiabilitiesNetMinorityInterest"
    RETAINED_EARNINGS = "RetainedEarnings"
    TOTAL_EQUITY = "StockholdersEquity"
    NET_DEBT = "NetDebt"
    WORKING_CAPITAL = "WorkingCapital"

class IncomeStatementMetric(str, Enum):
    TOTAL_REVENUE = "TotalRevenue"
    COST_OF_REVENUE = "CostOfRevenue"
    GROSS_PROFIT = "GrossProfit"
    R_AND_D = "ResearchAndDevelopment"
    SG_AND_A = "SellingGeneralAndAdministration"
    TOTAL_OPERATING_EXPENSES = "OperatingExpense"
    OPERATING_INCOME = "OperatingIncome"
    EBITDA = "EBITDA"
    PRETAX_INCOME = "PretaxIncome"
    NET_INCOME = "NetIncome"
    EPS_BASIC = "BasicEPS"
    EPS_DILUTED = "DilutedEPS"   

class CashFlowMetric(str, Enum):
    OPERATING_CASH_FLOW = "OperatingCashFlow"
    NET_INCOME = "NetIncomeFromContinuingOperations"
    DEPRECIATION_AMORTIZATION = "DepreciationAndAmortization"
    STOCK_BASED_COMP = "StockBasedCompensation"
    CAPITAL_EXPENDITURE = "CapitalExpenditure"
    INVESTING_CASH_FLOW = "InvestingCashFlow"
    SALE_PURCHASE_INVESTMENT = "NetInvestmentPurchaseAndSale"
    FINANCING_CASH_FLOW = "FinancingCashFlow"
    DIVIDENDS_PAID = "CashDividendsPaid"
    REPURCHASE_OF_STOCK = "RepurchaseOfCapitalStock"
    FREE_CASH_FLOW = "FreeCashFlow"     

class TenKFilingToolState(BaseModel):
    query : str
    tickers : List[str] = Field(...,description='List of targetted tickers.')
    years : List[str] = Field(...,description="List of years e.g.['2024','2023']")
    sections : List[TenKSECSection] = Field(...,
                                            description="""
    'i-1' : Company operations, products, services, markets, strategy.
    'i-1a' : Major risks affecting business, finances, or operations.
    'i-2' : Physical assets like offices, plants, warehouses.
    'i-3' : Major lawsuits or regulatory cases.
    'i-4' : Mining-related safety reporting (if applicable).
    'ii-5' : Stock info, dividends, shareholders.
    'ii-6 : Historical financial summary.
    'ii-7' : Management explanation of financial performance and outlook.
    'ii-7a' : Interest rate, currency, commodity risk exposure.
    'ii-9' : Accounting disputes (if any).
    'ii-9A' : Internal controls over financial reporting.
    'ii-9B' : Miscellaneous disclosures.
    'iii-10' : Leadership and governance structure.
    'iii-11' : Salary, bonuses, stock compensation.
    'iii-12' : Major shareholders and insider ownership.
    'iii-13' : Conflicts of interest or insider dealings.
    'iii-14' : Audit and consulting fees.
    'iv-15' : Contracts, certifications, supporting filings.
                                            """)
    

class TenQFilingToolState(BaseModel):
    query : str
    tickers : List[str] = Field(...,description='List of targetted tickers.')
    years : List[str] = Field(...,description="List of years e.g.['2024','2023']")
    sections : List[TenQSECSection] = Field(...,
                                            description="""
'1'  : Unaudited financial statements and notes for the quarter.
'2'  : Management explanation of quarterly performance and changes.
'3'  : Exposure to market risks (interest rates, FX, commodities).
'4'  : Disclosure controls and internal control procedures.

'2-1'  : Material legal proceedings during the quarter.
'2-1A: Updated risk factors (only if there are material changes).
'2-2'  : Unregistered securities sales and share repurchases.
'2-3'  : Defaults on senior securities (if any).
'2-4'  : Mine safety disclosures (if applicable).
'2-5'  : Other material information not previously reported.
'2-6'  : Exhibits, certifications, and attachments.""")
    
class CashFlowToolState(BaseModel):
   tickers : List[str]
   years : List[str]
   values : List[CashFlowMetric]

class IncomeStatementToolState(BaseModel):
   tickers : List[str]
   years : List[str]
   values : List[IncomeStatementMetric]

class BalanceSheetToolState(BaseModel):
   tickers : List[str]
   years : List[str]
   values : List[BalanceSheetMetric]

class RealTimeToolState(BaseModel):
    tickers : List[str] 
    period : str
    data_type : List[str]

class SearchToolState(BaseModel):
    query : str = Field(...,description="The information that we want to get from the internet.")

class TickerResolverState(BaseModel):
    company_names : List[str] = Field(...,description = "This is the list of all the companies whose ticker we want to extract" \
    "to solve the query.")

class NewsToolState(BaseModel):
    tickers : List[str]




    



