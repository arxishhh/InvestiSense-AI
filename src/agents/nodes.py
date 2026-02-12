from dotenv import load_dotenv
from src.agents.states import AgentState
from langgraph.types import Command
from src.agents.utils import format_proofs
from src.agents.service import get_prompt
from langchain_core.prompts import PromptTemplate
from src.agents.service import build_tools
from src.agents.executor import tool_call_loop
from langchain_groq import ChatGroq
import logging

load_dotenv()
tools = build_tools()
AuditTools = tools.get('AuditorTools',[])
FinancerTools = tools.get('FinancerTools',[])
NewsRoomTools = tools.get('NewsRoomTools',[])

llm = ChatGroq(
    model='openai/gpt-oss-120b'
)

def supervisor_node(state : AgentState):
    pass

def auditor_node(state : AgentState):

    query = state.get('query')
    template = get_prompt('auditor')
    message = ""
    proofs = []
    done = False

    iterations = 0

    prompt = PromptTemplate(
        template=template,
        input_variables=['query','proofs']
    )

    while not done and iterations <= 5:
        invoke_prompt = prompt.invoke(
            {'query':query,'proofs':message}
        )

        llm_with_tools = llm.bind_tools(AuditTools)
        response = llm_with_tools.invoke(invoke_prompt)

        if response.content == 'DONE' or not response.tool_calls:
            done = True
            
        else :
            tool_calls = response.tool_calls
            tool_response = tool_call_loop(tool_calls=tool_calls)
            message = message + tool_response.get('message')
            proofs = proofs+tool_response.get('proofs',[])

        iterations+=1
    
    state['proofs'] = state.get('proofs',"")+proofs
    state['formatted_proof'] = state.get('formatted_proof',"")+format_proofs(proofs)
    return state

def financer_node(state : AgentState):
    query = state.get('query')
    template = get_prompt('financer')
    message = ""
    proofs = []
    done = False

    iterations = 0

    prompt = PromptTemplate(
        template=template,
        input_variables=['query','proofs']
    )

    while not done and iterations <= 5:
        invoke_prompt = prompt.invoke(
            {'query':query,'proofs':message}
        )

        llm_with_tools = llm.bind_tools(FinancerTools)
        response = llm_with_tools.invoke(invoke_prompt)

        if response.content == 'DONE' or not response.tool_calls:
            done = True
            
        else :
            tool_calls = response.tool_calls
            tool_response = tool_call_loop(tool_calls=tool_calls)
            message = message + tool_response.get('message')
            proofs = proofs+tool_response.get('proofs',[])

        iterations+=1
    
    state['proofs'] = state.get('proofs',"")+proofs
    state['formatted_proof'] = state.get('formatted_proof',"")+format_proofs(proofs)
    return state

def newsroom_node(state : AgentState):

    query = state.get('query')
    template = get_prompt('newsroom')
    message = ""
    proofs = []
    done = False

    iterations = 0

    prompt = PromptTemplate(
        template=template,
        input_variables=['query','proofs']
    )

    while not done and iterations <= 5:
        invoke_prompt = prompt.invoke(
            {'query':query,'proofs':message}
        )

        llm_with_tools = llm.bind_tools(NewsRoomTools)
        response = llm_with_tools.invoke(invoke_prompt)

        if response.content == 'DONE' or not response.tool_calls:
            done = True
            
        else :
            tool_calls = response.tool_calls
            tool_response = tool_call_loop(tool_calls=tool_calls)
            message = message + tool_response.get('message')
            proofs = proofs+tool_response.get('proofs',[])

        iterations+=1
    
    state['proofs'] = state.get('proofs',"")+proofs
    state['formatted_proof'] = state.get('formatted_proof',"")+format_proofs(proofs)
    return state


def analyzer_node(state : AgentState):

    proofs = state.get("formatted_proof"," ")
    template = get_prompt('analyser')

    prompt = PromptTemplate(
        template=template,
        input_variables=['query','proofs']
    )
    invoke_prompt = prompt.invoke({'query':state.get('query'," "),
                                   'proofs':proofs})
    
    response = llm.invoke(invoke_prompt)

    state['analysis'] = response.content

    return state



def replier_node(state : AgentState):
    
    query = state.get('query'," ")
    analysis = state.get('analysis'," ")

    template = get_prompt('replier')

    prompt = PromptTemplate(
        template=template,
        input_variables=['query','analysis']
    )
    invoke_prompt = prompt.invoke({'query':query,'analysis':analysis})

    try:
        response = llm.invoke(invoke_prompt)
    except Exception as e:
        logging.error(str(e))

    state['final_response'] = response.content
    return state


if __name__ == "__main__":
    state = newsroom_node({
        'query':"Why is NVDA volatile today despite positive news?",
        'proofs':[],
        'formatted_proof':"",})
    state = analyzer_node(state)
    print(state['analysis'])
    print(replier_node(state)['final_response'])
    