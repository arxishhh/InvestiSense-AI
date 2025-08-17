import sqlite3
from pathlib import Path
import pandas as pd
import asyncio
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from backend.utils.routing_classifier_filter import answer_generator
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
import os
import re


load_dotenv()
parser = StrOutputParser()
llm = ChatGroq(model_name = os.getenv('OPENAI_MODEL'))

async def generate_sql_query(query,role):
    prompt = PromptTemplate(
        template = '''You are an expert in understanding the database schema and generating SQL queries for a natural language question
        pertaining to the data you have.The schema is provided in the schema tags.
        <schema>
        table: {role}
        Company (TEXT) → Name of the company. Example: "Apple Inc.".
        Ticker (TEXT) → Stock ticker symbol of the company. Example: "AAPL".
        Fiscal_Year (INTEGER) → The year of the company’s fiscal reporting period. Example: 2024.
        Fiscal_Period (TEXT) → Quarter or full-year reporting period. Example: "FY","Q1","Q2","Q3".
        Filing_Date (DATE) → Date the financial report was officially filed. Format: YYYY-MM-DD.
        Start_Date (DATE) → Start date of the reporting period. Format: YYYY-MM-DD.
        End_Date (DATE) → End date of the reporting period. Format: YYYY-MM-DD.
        Assets (NUMERIC) → Total assets at period end.
        Liabilities (NUMERIC) → Total liabilities at period end.
        Equity (NUMERIC) → Shareholders’ equity at period end.
        Revenues (NUMERIC) → Total revenue for the period.
        Net_Income (NUMERIC) → Profit after all expenses, taxes, and interest.
        Basic_EPS (NUMERIC) → Basic earnings per share.
        Diluted_EPS (NUMERIC) → Diluted earnings per share (after considering stock dilution).
        Gross_Profit (NUMERIC) → Revenue minus cost of goods sold.
        Operating_Income (NUMERIC) → Profit from core business operations before taxes and interest.
        Cash_Flow_Operating (NUMERIC) → Net cash from operating activities.
        Cash_Flow_Investing (NUMERIC) → Net cash from investing activities.
        Cash_Flow_Financing (NUMERIC) → Net cash from financing activities.
        Gross_Margin (NUMERIC) → Gross profit ÷ revenue × 100 (%).
        Operating_Margin (NUMERIC) → Operating income ÷ revenue × 100 (%).
        Net_Margin (NUMERIC) → Net income ÷ revenue × 100 (%).
        ROA (NUMERIC) → Return on assets: net income ÷ total assets × 100 (%).
        ROE (NUMERIC) → Return on equity: net income ÷ shareholders’ equity × 100 (%).
        Debt_Ratio (NUMERIC) → Total liabilities ÷ total assets.
        Debt_To_Equity_Ratio (NUMERIC) → Total liabilities ÷ shareholders’ equity.
        </schema>
        Make sure whenever you try to search for the Company name the name can be in any case.
        So, make sure to use %LIKE% to fin the brand in condition. Never us e "ILIKE".
        Create a single SQL query for the question provided.
        The query should start with SELECT you are not allowed to make any changes in the database no matter what the query says
        Just the SQL query is neede , nothing more.Always provide the SQL in between
        the <SQL></SQL> tags.
        #######
        Query: {query}
        ''',
        input_variables= ['query','role']
    )
    chain = prompt | llm | parser
    return await chain.ainvoke({'query':query,'role':role})
async def run_query(query,role):
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    db_path = BASE_DIR/'database'/'numeric_db'/f'{role}_data.db'
    if not db_path.exists():
        raise FileNotFoundError(f"Database file not found: {db_path}")
    if query.strip().upper().startswith('SELECT'):
        with sqlite3.connect(str(db_path)) as conn:
            try:
                df = pd.read_sql_query(query, conn)
            except Exception as e:
                return 'The specified role do not have the access to the following data.'
            return df

async def sql_chain(query,role):
    sql_query = await generate_sql_query(query,role)
    pattern = "<SQL>(.*?)</SQL>"
    match = re.findall(pattern,sql_query,re.DOTALL)
    if match:
         context = await run_query(match[0],role)
         context = context.to_markdown(index =False) if type(context) == pd.core.frame.DataFrame else context
    else:
        context = 'No information avaliable.'
    return await answer_generator(query,context,role)
if __name__ == '__main__':
    print(asyncio.run(sql_chain('Show me the latest quarterly revenue and net income figures for Apple for the years 2022 and 2023, and compare their gross margin percentages over the same periods.','analyst')))