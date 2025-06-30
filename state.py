from typing import TypedDict, Optional, List, Dict, Any

class EnhancedAgentState(TypedDict):
    """
    Enhanced state that tracks the entire content creation pipeline.
    Each agent contributes to different fields in the state.
    """
    
    # Input
    topic: str
    
    # Research phase
    research_report: Optional[str]
    research_sources: Optional[List[Dict[str, str]]]
    
    # Writing phase  
    blog_post: Optional[str]
    
    # Editing phase
    edited_post: Optional[str]
    editing_notes: Optional[str]
    
    # Fact-checking phase
    final_post: Optional[str]
    fact_check_report: Optional[str]
    verified_claims: Optional[List[Dict[str, Any]]]
    
    # Metadata
    generation_timestamp: Optional[str]
    agent_notes: Optional[Dict[str, str]]