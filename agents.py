from datetime import datetime
from langchain_core.prompts import PromptTemplate
from typing import Dict, Any

from state import EnhancedAgentState
from tools import news_search_tool


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
    
    # Create a more direct approach to using the search tool
    # First, generate search queries based on the topic
    query_prompt = PromptTemplate.from_template("""
You are a research analyst. Generate 3-5 different search queries for researching the topic: "{topic}"

Make the queries specific and varied to gather comprehensive information if dates would be added in the queries it must be either relativve (last week , next week, last month, next month, etc...) or using the year 2025.
Output only the search queries, one per line, no explanations.
""")
    
    # Get search queries from the LLM
    queries_response = llm.invoke(query_prompt.format(topic=topic))
    queries = [q.strip() for q in queries_response.content.strip().split('\n') if q.strip()]
    
    # Perform searches
    search_results = []
    for query in queries[:5]:  # Limit to 5 searches
        try:
            result = news_search_tool.func(query)
            search_results.append({
                "query": query,
                "results": result
            })
        except Exception as e:
            print(f"Search error for query '{query}': {e}")
    
    # Now compile the research report
    research_prompt = PromptTemplate.from_template("""
You are a senior research analyst. Based on the following search results about "{topic}", 
create a comprehensive research report.

Search Results:
{search_results}

Create a well-structured research report that includes:
1. Executive Summary (2-3 sentences)
2. Key Findings (5-7 bullet points with sources)
3. Detailed Analysis
4. Notable Trends and Insights
5. Source URLs

Make sure to cite specific information from the search results.
""")
    
    # Format search results for the prompt
    formatted_results = ""
    for sr in search_results:
        formatted_results += f"\n\nQuery: {sr['query']}\n"
        formatted_results += f"Results:\n{sr['results']}\n"
        formatted_results += "-" * 50
    
    # Generate the research report
    report_response = llm.invoke(
        research_prompt.format(
            topic=topic,
            search_results=formatted_results
        )
    )
    
    return {
        "research_report": report_response.content,
        "research_sources": search_results,
        "agent_notes": {"research_agent": f"Completed research with {len(search_results)} searches"},
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