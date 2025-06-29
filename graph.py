from functools import partial
from langgraph.graph import StateGraph, END, START
from state import AgentState
from agents import research_node, writer_agent
from config import GOOGLE_API_KEY, MODEL_NAME
from langchain_google_genai import ChatGoogleGenerativeAI

def create_graph(temperature=0.3):
    """
    Creates and returns the LangGraph state machine.
    """
    llm = ChatGoogleGenerativeAI(model=MODEL_NAME, temperature=temperature, google_api_key=GOOGLE_API_KEY)

    # Define nodes with the LLM
    research_node_with_llm = partial(research_node, llm=llm)
    writer_agent_with_llm = partial(writer_agent, llm=llm)

    graph = StateGraph(AgentState)
    graph.add_node("researcher", research_node_with_llm)
    graph.add_node("writer", writer_agent_with_llm)
    graph.add_edge(START, "researcher")
    graph.add_edge("researcher", "writer")
    graph.add_edge("writer", END)
    return graph.compile()