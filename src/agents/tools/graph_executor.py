from langgraph.graph import START,END,StateGraph
from src.agents.nodes import *
from src.agents.states import AgentState

def intializing_graph() -> StateGraph:

    graph = StateGraph(AgentState)
    
    graph.add_node('supervisor',supervisor_node)
    graph.add_node('auditor',auditor_node)
    graph.add_node('financer',financer_node)
    graph.add_node('newsroom',newsroom_node)
    graph.add_node('analyzer',analyzer_node)
    graph.add_node('replier',replier_node)

    graph.add_edge(START,'supervisor')
    
    graph = graph.compile()
    return graph

graph = intializing_graph()