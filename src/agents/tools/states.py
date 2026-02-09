from typing import TypedDict,Dict,List
from pydantic import BaseModel,Field
from langchain_core.messages import BaseMessage
from uuid import UUID
from enum import Enum

class AgentState(TypedDict):
    session_id : UUID = Field(default = UUID)

    query : str
    final_response : str
    messages : List[BaseMessage]
    #WebSockets
    status : str = Field(default = "intermediate")
    current_process : str
    #Context
    proofs : List[Dict[str,str]]



class TenKSECSection(str, Enum):
    BUSINESS = "1"             
    RISK_FACTORS = "1A"        
    UNRESOLVED_STAFF_COMMENTS = "1B"
    PROPERTIES = "2"           
    LEGAL_PROCEEDINGS = "3" 
    MINE_SAFETY = "4"
    MARKET_FOR_EQUITY = "5"     
    RESERVED_6 = "6"          
    MDA = "7"                  
    MARKET_RISK = "7A"         
    ACCOUNTING_DISPUTES = "9"   
    INTERNAL_CONTROLS = "9A"    
    OTHER_INFO = "9B"          
    FOREIGN_AUDIT = "9C"      
    DIRECTORS_GOVERNANCE = "10" 
    EXECUTIVE_COMP = "11"     
    SECURITY_OWNERSHIP = "12"  
    CERTAIN_RELATIONSHIPS = "13"
    AUDIT_FEES = "14"         
    EXHIBITS = "15"


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
    '1' : Company operations, products, services, markets, strategy.
    '1A' : Major risks affecting business, finances, or operations.
    '2' : Physical assets like offices, plants, warehouses.
    '3' : Major lawsuits or regulatory cases.
    '4' : Mining-related safety reporting (if applicable).
    '5' : Stock info, dividends, shareholders.
    '6 : Historical financial summary.
    '7' : Management explanation of financial performance and outlook.
    '7A' : Interest rate, currency, commodity risk exposure.
    '9' : Accounting disputes (if any).
    '9A' : Internal controls over financial reporting.
    '9B' : Miscellaneous disclosures.
    '9C' : Disclosure about foreign audit inspections.
    '10' : Leadership and governance structure.
    '11' : Salary, bonuses, stock compensation.
    '12' : Major shareholders and insider ownership.
    '13' : Conflicts of interest or insider dealings.
    '14' : Audit and consulting fees.
    '15' : Contracts, certifications, supporting filings.
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

class AuditorState(BaseModel):
    query : str
    done : bool 
    iterations : int = 0


    



