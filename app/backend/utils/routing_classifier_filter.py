import os
from langchain_groq import ChatGroq
from langchain_core.runnables import RunnableParallel,RunnablePassthrough
from langchain_core.output_parsers import JsonOutputParser
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

import warnings
warnings.filterwarnings('ignore')

load_dotenv()

model = ChatGroq(model_name = os.getenv('OPENAI_MODEL'))
parser_json = JsonOutputParser()
parser_str = StrOutputParser()

async def routing(**kwargs):
    """Route a user's query into numerical, textual, real-time, and general categories.

    Args:
        **kwargs: Keyword arguments, including 'query' (str): The user's query to be routed.

    Returns:
        dict: A JSON object with keys 'Numerical Query', 'Textual Query', 'Real-Time Query', and 'General Query' representing the categorized queries.
    """
    query = kwargs['query']
    prompt = PromptTemplate(
        template='''
You are a query classifier for a fintech platform.
Split the user's query into exactly 4 categories:
Numerical Query: Past numerical data, metrics, stats, financial figures.
Textual Query: Qualitative descriptions, summaries, reviews, definitions, explanations, overviews.
Real-Time Query: Present/current data, live updates, today's information.
General Query:A general query refers to a normal conversational input or a question that does not directly involve stock tickers, data types (like price, volume, etc.), or any simple definiton related to financial-domain or any structured market-related information. These queries are more open-ended, context-seeking, or outside the scope of financial data tools.
Rules:
Full Coverage: Every word must belong to exactly one category.
Context Preservation: Each sub-query must repeat company names, dates, and metrics from the original query so it can be executed independently.
Year Inclusion: If the query mentions or implies a year, include it explicitly in every relevant sub-query.
General Query: If a query is asking to explain a term which is common in  financial domain it should be a general query
Empty String: Use "" if not applicable.
Output Format: Return only JSON with keys Numerical Query, Textual Query, Real-Time Query.
Example
Input: "Compare Apple and Microsoft risk factors and financial statements from 2022 and 2023 10-Ks"
Output:
  "Numerical Query": "Provide Apple's and Microsoft's financial statements from 2022 and 2023 10-K filings.",
  "Textual Query": "Summarize Apple's and Microsoft's risk factors from 2022 and 2023 10-K filings.",
  "Real-Time Query": ""
  "General Query": ""
Query: {query}
The Format should be {format}
        ''',
        input_variables=['query'],
        partial_variables={'format': parser_json.get_format_instructions()})
    chain = prompt | model | parser_json
    return await chain.ainvoke({'query': query})

async def filter(**kwargs):
    """Parse a financial query related to SEC 10-K filings and extract relevant information.

    Args:
        **kwargs: Keyword arguments, must include 'query' for the input query string.

    Returns:
        dict: A JSON object with the following keys:
            'ticker' (list): Stock tickers as an array, or [null] if none.
            'year' (list): Fiscal years as an array, or [null] if none.
            'sec' (list): 10-K section(s) as an array, options include:
                - Business Overview
                - Risk Factors
                - Management's Discussion and Analysis
                - Mergers & Acquisitions
                - Legal Proceedings
                - Controls and Procedures
                - Market Risk

    Examples:
        Input: "Show me Apple's business overview from their 2023 10-K"
        Output: {"ticker": ["AAPL"], "year": ["2023"], "sec": ["Business Overview"]}
        Input: "What are the risk factors in Tesla's latest annual report?"
        Output: {"ticker": ["TSLA"], "year": ["2025"], "sec": ["Risk Factors"]}
    """
    query = kwargs['query']
    prompt_filter = PromptTemplate(
        template='''
        You are a financial query parser for SEC 10-K filings. Extract and return ONLY a structured JSON with:
ticker: Stock tickers as an array (e.g., ["AAPL"]). [null] if none.
year: Fiscal years as an array (e.g., [2023]). [null] if none.
section: 10-K section(s) as an array. Options:
Business Overview, Risk Factors,Management's Discussion and Analysis, Mergers & Acquisitions, Legal Proceedings, Controls and Procedures,Market Risk
Rules:
Detect tickers or company names → map to tickers.
Identify fiscal years or relative references (e.g., "latest", "last year").
Map intent to closest section(s); include multiple if applicable.
Output only the JSON object with all fields as arrays.
Examples:(Follow the format of the examples strictly the entires should be 'ticker','year','sec'
Input: Show me Apple's business overview from their 2023 10-K
Output: "ticker":["AAPL"],"year":['2023'],"sec":["Business Overview"]
Input: What are the risk factors in Tesla's latest annual report?
Output: "ticker":["TSLA"],"year":['2025'],"sec":["Risk Factors"]
Input: Analyze Amazon's management discussion and analysis section
Output: "ticker":["AMZN"],"year":[null],"sec":["Management's Discussion and Analysis"]
Input: Summarize all ongoing lawsuits and legal disputes mentioned in Apple’s 2023 Form 10-K.
Output: "ticker": ["TSLA"],"year": ["2021"],"sec": ["Controls and Procedures"]
Input: Show me any regulatory investigations or litigation risks disclosed by Amazon in its 2022 annual SEC report.
Output: "ticker": ["AMZN"],"year": ["2022"],"sec": ["Legal Proceedings"]
Input: Retrieve the qualitative and quantitative disclosures about market risk for Meta from its 2023 10-K filing.
Output: "ticker": ["META"],"year": ["2023"],"sec": ["Market Risks"]
Input: Extract Apple’s auditor attestation and Sarbanes-Oxley compliance discussion about internal controls from its 2021 annual SEC report.
Output: "ticker": ["AAPL"],"year": ["2021"],"sec": ["Controls and Procedures"]
The format of the output should be {format}.
##########
Query
{query}
    ''',
        input_variables=['query', 'format'],
        partial_variables={'format': parser_json.get_format_instructions()}
    )
    parallel_chain = RunnableParallel({
        'Refined': RunnablePassthrough(),
        'Filter': prompt_filter | model | parser_json
    })
    chain = parallel_chain
    return await chain.ainvoke({'query':query})
async def answer_generator(**kwargs):
    """Generate a user-friendly answer to a query based on provided context.

    Args:
        **kwargs: Keyword arguments containing the query, context, and role.
            query (str): The query to be answered.
            context (str): The context or data related to the query.
            role (str): The role of the responder (e.g., a finance professional).

    Returns:
        str: A formatted answer to the query based on the provided context.
    """
    query, context, role = kwargs['query'], kwargs['context'], kwargs['role']
    prompt = PromptTemplate(
        template = '''You are a highly professional {role} in a big finance company.
        Answer the following query you will be given a list which is a direct answer to the query.
        You just have to frame it in a good and readible way.Make it more user friendly.Try to use all the data given in the data.You have to strictly 
        answer according to the data and if no value is provided don't answer the question.If the message says no information available answer that by rephrasing no need to make up things on your own.
        #####
        Query: {query}
        #####
        Data: {data}
        ''',
        input_variables= ['query','role','context']
    )
    chain = prompt | model | parser_str
    return await chain.ainvoke({'query':query,'role':role,'data':context})
async def answer_general_query(**kwargs):
    """Answer a general query from the perspective of a specific role in a finance company.

    Args:
        **kwargs: Keyword arguments.
            query (str): The query to be answered.
            role (str): The role of the respondent.

    Returns:
        str: A professional and concise response to the query.
    """
    query, role = kwargs['query'], kwargs['role']
    prompt = PromptTemplate(
        template='''You are a highly professional {role} in a big finance company.
            Answer the following query
            You just have to frame it in a good and readible way.Make it more user friendly.Make it short and precise.
            #####
            Query: {query}
            ''',
        input_variables=['query', 'role']
    )
    chain = prompt | model | parser_str
    return await chain.ainvoke({'query': query, 'role': role})



