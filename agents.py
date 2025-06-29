from langchain_core.prompts import PromptTemplate
from langgraph.prebuilt import create_react_agent

from config import TOPIC, RESEARCH_REPORT, BLOG_POST
from tools import news_search_tool
from state import AgentState

# Define prompts
research_prompt_template = PromptTemplate.from_template("""
You are a senior research analyst. Your task is to research the following topic: "{input}".
You are great at finding the latest and most relevant news and developments on any given topic.
Your research report should be a concise summary of your findings, including the most important facts, figures, and trends.
Please provide at least 3-5 key bullet points and include the source URLs for each piece of information.
Your final output must be a well-written research report.
""")

writer_prompt_template = PromptTemplate(
    input_variables=[TOPIC, RESEARCH_REPORT],
    template="""
You are a tech content writer. Your task is to write a blog post on the topic: "{topic}".
You will be given a research report with facts and findings.
Your blog post should be engaging, easy to read, and informative.
Use the research report to create a compelling narrative.
The tone of the blog post should be slightly informal and tech-savvy.
Your final output must be a well-written blog post of at least 3 paragraphs.
"""
)

# Define agent nodes
def research_node(state: AgentState, llm) -> dict:
    topic = state[TOPIC]
    tools = [news_search_tool]

    agent = create_react_agent(
        llm,
        tools=tools,
    )

    result = agent.invoke(
        {"messages": [("user", research_prompt_template.format(input=topic))]}
    )

    return {RESEARCH_REPORT: result['messages'][-1].content}

def writer_agent(state: AgentState, llm) -> dict:
    topic = state[TOPIC]
    research = state[RESEARCH_REPORT]
    full_prompt = writer_prompt_template.format(topic=topic, research=research)
    response = llm.invoke(full_prompt)
    return {BLOG_POST: response.content}