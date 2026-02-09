from src.agents.tools.states import AgentState
from langgraph.types import Command
from src.agents.utils import create_auditor_state



def supervisor_node(state : AgentState):
    pass

def auditor_node(state : AgentState):
    auditor_state = create_auditor_state(state.get('query'))

    while not auditor_state.get('done'):
        pass

def financer_node(state : AgentState):
    pass

def newsroom_node(state : AgentState):
    pass

def analyzer_node(state : AgentState):
    pass

def replier_node(state : AgentState):
    pass