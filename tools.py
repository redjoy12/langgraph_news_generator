from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_core.tools import Tool
from config import SERPER_API_KEY

def get_news_search_tool() -> Tool:
    """
    Creates and returns a tool for searching recent news.
    """
    search = GoogleSerperAPIWrapper(api_key=SERPER_API_KEY, k=5, type="news", tbs="qdr:d")

    def news_search_tool_func(query: str) -> str:
        """
        Performs a news search and formats the results.
        """
        try:
            results = search.results(query)
            news_items = results.get("news", [])[:5]

            if not news_items:
                return f"No recent news articles found for query: '{query}'"

            formatted_results = []
            for i, item in enumerate(news_items, start=1):
                title = item.get("title", "No title")
                snippet = item.get("snippet", "No summary")
                link = item.get("link", "No URL")
                date = item.get("date", "No date")
                formatted_results.append(
                    f"{i}. **{title}**\n"
                    f"   Date: {date}\n"
                    f"   Summary: {snippet}\n"
                    f"   Link: {link}\n"
                )

            return "\n".join(formatted_results)
        except Exception as e:
            return f"Error searching for '{query}': {str(e)}"

    return Tool(
        name="search",
        func=news_search_tool_func,
        description="Search for the most recent news (past 24 hours) on a topic. Returns titles, summaries, dates, and links."
    )

news_search_tool = get_news_search_tool()