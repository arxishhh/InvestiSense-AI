from edgar import *
from langchain_classic.chains import MapReduceDocumentsChain
from langchain_classic.chains.llm import LLMChain
from langchain_text_splitters import CharacterTextSplitter
from src.agents.service import get_prompt
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from src.config import Config

load_dotenv()

set_identity("arxishhh@gmail.com")
llm = ChatGroq(
    model=Config.GROQ_MODEL
)

def get_filing_text(query : str,ticker : str, years : List[str], sections : List[str])-> str:
    company = Company(ticker)
    filings = company.get_filings(form = '10-K')
    filtered_filings = [
        f for f in filings for y in years if y in str(f.filing_date)
    ]
    context = [
        "Ticker : "+ticker+"\n"+str(f.filing_date)+f.obj()[f'Item {section}'] for section in sections for f in filtered_filings
    ]
    context = "\n".join(context)
    summarized_context = summarizing_context(context)
    return summarized_context

def summarizing_context(query : str,context : str):
    map_template = get_prompt('map').format(query = query)
    reduce_template = get_prompt('reduce').format(query = query)

    map_prompt = PromptTemplate.from_template(
        prompt = map_template
    )
    reduce_prompt = PromptTemplate.from_template(
        prompt = reduce_template
    )

    map_chain = LLMChain(
        prompt=map_prompt,
        llm=llm
    )

    reduce_chain = LLMChain(
        prompt=reduce_prompt,
        llm=llm
    )

    map_reduce_chain = MapReduceDocumentsChain(
        llm_chain=map_chain,
        reduce_documents_chain=reduce_chain,

    )






if __name__ == "__main__":
    print(get_filing_text("","AAPL",['2025','2024'],["1"]))
