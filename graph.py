from functools import partial
from langgraph.graph import StateGraph, END, START
from state import EnhancedAgentState
from agents import (
    research_node, 
    writer_node, 
    editor_node, 
    fact_checker_node
)
from config import GOOGLE_API_KEY, MODEL_NAME
from langchain_google_genai import ChatGoogleGenerativeAI

def create_enhanced_graph(temperature=0.3, streaming=False):
    """
    Creates and returns the enhanced LangGraph state machine with multiple specialized agents.
    
    Args:
        temperature: The temperature for the LLM
        streaming: Whether to enable streaming mode
    """
    
    # Initialize LLM
    llm = ChatGoogleGenerativeAI(
        model=MODEL_NAME, 
        temperature=temperature, 
        google_api_key=GOOGLE_API_KEY
    )

    # Create specialized agent nodes with LLM
    research_agent = partial(research_node, llm=llm)
    writer_agent = partial(writer_node, llm=llm)
    editor_agent = partial(editor_node, llm=llm)
    fact_checker_agent = partial(fact_checker_node, llm=llm)

    # Build the graph
    graph = StateGraph(EnhancedAgentState)
    
    # Add nodes
    graph.add_node("researcher", research_agent)
    graph.add_node("writer", writer_agent)
    graph.add_node("editor", editor_agent)
    graph.add_node("fact_checker", fact_checker_agent)
    
    # Define the workflow
    graph.add_edge(START, "researcher")
    graph.add_edge("researcher", "writer")
    graph.add_edge("writer", "editor")
    graph.add_edge("editor", "fact_checker")
    graph.add_edge("fact_checker", END)
    
    # Compile and return
    compiled_graph = graph.compile()
    
    return compiled_graph