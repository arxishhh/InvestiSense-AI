from dotenv import load_dotenv
from src.agents.states import AgentState,SupervisorState
from langgraph.types import Command
from src.agents.utils import format_proofs
from src.agents.service import get_prompt
from langchain_core.prompts import PromptTemplate
from src.agents.service import build_tools
from src.agents.executor import tool_call_loop
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.types import Command
import logging
import os

load_dotenv()
tools = build_tools()
AuditTools = tools.get('AuditorTools',[])
FinancerTools = tools.get('FinancerTools',[])
NewsRoomTools = tools.get('NewsRoomTools',[])

llm = ChatGroq(
    model='openai/gpt-oss-120b'
)
supervisorLLM = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    google_api_key=os.getenv('GEMINI_API_KEY')
)

def supervisor_node(state : AgentState):
    template = get_prompt("supervisor")
    status_messages = state.get('status_messages',"")
    history = state.get('formatted_history',"")


    prompt = PromptTemplate(
        template=template,
        input_variables=['query','proofs','history']
    )

    invoke_prompt = prompt.invoke({
        'query':state['query'],
        'proofs':status_messages,
        'history':history
    })
    response = supervisorLLM.with_structured_output(SupervisorState).invoke(invoke_prompt)
    goto = [res.value for res in response.route]
    return Command(
        goto=goto
    )

def auditor_node(state : AgentState):

    query = state.get('query')
    template = get_prompt('auditor')
    messages = ""
    proofs = []
    done = False

    iterations = 0

    prompt = PromptTemplate(
        template=template,
        input_variables=['query','proofs']
    )

    while not done and iterations <= 5:
        invoke_prompt = prompt.invoke(
            {'query':query,'proofs':messages}
        )

        llm_with_tools = llm.bind_tools(AuditTools)
        response = llm_with_tools.invoke(invoke_prompt)

        if response.content == 'DONE' or not response.tool_calls:
            done = True
            
        else :
            tool_calls = response.tool_calls
            tool_response = tool_call_loop(tool_calls=tool_calls)
            messages = f"{messages}  {tool_response.get('message')}"
            proofs = proofs+tool_response.get('proofs',[])

        iterations+=1
    
    
    formatted_proofs = state['formatted_proofs']+"\n"+format_proofs(proofs)
    proofs = state['proofs']+proofs
    status_messages =  state['status_messages']+" "+messages


    return Command(
        goto='supervisor',
        update={
                "proofs":proofs,
                "formatted_proofs":formatted_proofs,
                "status_messages":status_messages
        })

def financer_node(state : AgentState):
    query = state.get('query')
    template = get_prompt('financer')
    messages = ""
    proofs = []
    done = False

    iterations = 0

    prompt = PromptTemplate(
        template=template,
        input_variables=['query','proofs']
    )

    while not done and iterations <= 5:
        invoke_prompt = prompt.invoke(
            {'query':query,'proofs':messages}
        )

        llm_with_tools = llm.bind_tools(FinancerTools)
        response = llm_with_tools.invoke(invoke_prompt)

        if response.content == 'DONE' or not response.tool_calls:
            done = True
            
        else :
            tool_calls = response.tool_calls
            tool_response = tool_call_loop(tool_calls=tool_calls)
            messages = f"{messages}  {tool_response.get('message')}"
            proofs = proofs+tool_response.get('proofs',[])

        iterations+=1
        
    formatted_proofs = state['formatted_proofs']+"\n"+format_proofs(proofs)
    proofs = state['proofs']+proofs
    status_messages =  state['status_messages']+" "+messages

    return Command(
        goto='supervisor',
        update={
                "proofs" : proofs,
                "formatted_proofs" : formatted_proofs,
                "status_messages" : status_messages
        })

def newsroom_node(state : AgentState):

    query = state.get('query')
    template = get_prompt('newsroom')
    messages = ""
    proofs = []
    done = False

    iterations = 0

    prompt = PromptTemplate(
        template=template,
        input_variables=['query','proofs']
    )

    while not done and iterations <= 5:
        invoke_prompt = prompt.invoke(
            {'query':query,'proofs':messages}
        )

        llm_with_tools = llm.bind_tools(NewsRoomTools)
        response = llm_with_tools.invoke(invoke_prompt)

        if response.content == 'DONE' or not response.tool_calls:
            done = True
            
        else :
            tool_calls = response.tool_calls
            tool_response = tool_call_loop(tool_calls=tool_calls)
            messages = f"{messages}  {tool_response.get('message')}"
            proofs = proofs+tool_response.get('proofs')

        iterations+=1

    proofs = state['proofs']+proofs
    formatted_proofs = f"{state['formatted_proofs']} \n {format_proofs(proofs)}"
    status_messages = f"{state['status_messages']} {messages}"
    return Command(
        goto='supervisor',
        update={
                "proofs" : proofs,
                "formatted_proofs" : formatted_proofs,
                "status_messages" : status_messages
        })


def analyzer_node(state : AgentState):

    proofs = state['formatted_proofs']
    template = get_prompt('analyser')

    prompt = PromptTemplate(
        template=template,
        input_variables=['query','proofs']
    )
    invoke_prompt = prompt.invoke({'query':state['query'],
                                   'proofs':proofs})
    
    response = llm.invoke(invoke_prompt)
    status_messages = f"{state['status_messages']} COMPLETED ANALYSIS ON THE GIVEN PROOFS."

    return Command(
        goto='replier',
        update={
                "analysis" : response.content,
                "status_messages" : status_messages
        })

def replier_node(state : AgentState):
    
    query = state['query']
    analysis = state['analysis']

    template = get_prompt('replier')

    prompt = PromptTemplate(
        template=template,
        input_variables=['query','analysis','history']
    )
    invoke_prompt = prompt.invoke({'query':query,'analysis':analysis,'history':state.get('formatted_history',"")})

    try:
        response = llm.invoke(invoke_prompt)
    except Exception as e:
        logging.error(str(e))

    state['final_response'] = response.content
    return state


if __name__ == "__main__":
    state = replier_node({
        'query':"Hi.",
        'proofs':[],
        'formatted_proofs':"",
        'status_messages':"",
        'analysis':""
        })
    print(state)