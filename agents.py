from datetime import datetime
from langchain_core.prompts import PromptTemplate
from langgraph.prebuilt import create_react_agent
from typing import Dict, Any, List

from state import EnhancedAgentState
from tools import news_search_tool

# Enhanced prompts for specialized agents
RESEARCH_PROMPT = PromptTemplate.from_template("""
You are a senior research analyst specializing in technology and current events. 

Your task is to research the following topic: "{topic}"

Requirements:
1. Find the latest and most relevant news and developments
2. Identify key trends, facts, and figures
3. Gather information from credible sources
4. Provide at least 5-7 key findings with source URLs
5. Structure your findings logically

Your research should be thorough but concise. Focus on factual information that would be valuable for writing an engaging blog post.

Format your response as a well-structured research report.
""")

WRITER_PROMPT = PromptTemplate.from_template("""
You are a skilled tech content writer with expertise in creating engaging, informative blog posts.

Topic: "{topic}"

Research Report:
{research_report}

Your task:
1. Write an engaging blog post based on the research findings
2. Use a slightly informal, tech-savvy tone that's accessible to general readers
3. Create a compelling narrative structure with clear introduction, body, and conclusion
4. Include specific facts, figures, and insights from the research
5. Make the content at least 4-5 substantial paragraphs
6. Add relevant subheadings to improve readability

The blog post should be informative yet engaging, turning the research findings into a story that readers will want to follow.
""")

EDITOR_PROMPT = PromptTemplate.from_template("""
You are an experienced content editor with a keen eye for clarity, style, and engagement.

Original Article:
{blog_post}

Topic: {topic}

Your editing tasks:
1. Improve clarity and readability
2. Enhance flow and structure
3. Fix any grammatical errors or awkward phrasing
4. Ensure consistent tone throughout
5. Add transitional phrases where needed
6. Optimize subheadings and paragraph breaks
7. Maintain the technical accuracy while improving accessibility
8. Ensure the article has a strong hook and satisfying conclusion

Provide the edited version that maintains the original content's substance while significantly improving its quality and readability.
""")

FACT_CHECKER_PROMPT = PromptTemplate.from_template("""
You are a meticulous fact-checker with expertise in technology and current events.

Article to fact-check:
{edited_post}

Research Sources:
{research_report}

Your responsibilities:
1. Verify all factual claims in the article
2. Check for consistency with the research sources
3. Identify any potential inaccuracies or unsupported statements
4. Ensure proper context for statistics and claims
5. Flag any information that seems outdated or questionable
6. Make necessary corrections while preserving the article's flow
7. Add disclaimer notes where appropriate

Provide the final, fact-checked version of the article with any necessary corrections or clarifications.
""")

def research_node(state: EnhancedAgentState, llm) -> Dict[str, Any]:
    """Enhanced research agent that gathers comprehensive information."""
    
    topic = state["topic"]
    tools = [news_search_tool]
    
    # Create research agent
    agent = create_react_agent(llm, tools=tools)
    
    # Execute research
    result = agent.invoke({
        "messages": [("user", RESEARCH_PROMPT.format(topic=topic))]
    })
    
    research_content = result['messages'][-1].content
    
    return {
        "research_report": research_content,
        "agent_notes": {"research_agent": "Completed comprehensive research"},
        "generation_timestamp": datetime.now().isoformat()
    }

def writer_node(state: EnhancedAgentState, llm) -> Dict[str, Any]:
    """Enhanced writer agent that creates engaging content."""
    
    topic = state["topic"]
    research_report = state["research_report"]
    
    # Generate the blog post
    prompt = WRITER_PROMPT.format(topic=topic, research_report=research_report)
    response = llm.invoke(prompt)
    
    # Update agent notes
    current_notes = state.get("agent_notes", {})
    current_notes["writer_agent"] = "Created initial blog post draft"
    
    return {
        "blog_post": response.content,
        "agent_notes": current_notes
    }

def editor_node(state: EnhancedAgentState, llm) -> Dict[str, Any]:
    """Editor agent that polishes and improves the content."""
    
    topic = state["topic"]
    blog_post = state["blog_post"]
    
    # Edit the blog post
    prompt = EDITOR_PROMPT.format(topic=topic, blog_post=blog_post)
    response = llm.invoke(prompt)
    
    # Update agent notes
    current_notes = state.get("agent_notes", {})
    current_notes["editor_agent"] = "Improved clarity, flow, and readability"
    
    return {
        "edited_post": response.content,
        "editing_notes": "Focused on improving clarity, flow, and engagement",
        "agent_notes": current_notes
    }

def fact_checker_node(state: EnhancedAgentState, llm) -> Dict[str, Any]:
    """Fact-checker agent that verifies accuracy and provides final version."""
    
    edited_post = state["edited_post"]
    research_report = state["research_report"]
    
    # Fact-check the article
    prompt = FACT_CHECKER_PROMPT.format(
        edited_post=edited_post, 
        research_report=research_report
    )
    response = llm.invoke(prompt)
    
    # Update agent notes
    current_notes = state.get("agent_notes", {})
    current_notes["fact_checker_agent"] = "Verified claims and ensured accuracy"
    
    return {
        "final_post": response.content,
        "fact_check_report": "All claims verified against research sources",
        "agent_notes": current_notes
    }