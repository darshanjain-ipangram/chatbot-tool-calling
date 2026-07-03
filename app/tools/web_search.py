from langchain_core.tools import tool
from ddgs import DDGS

@tool
def web_search(query: str) -> str:
    """Search the web for current events, news, or factual information."""
    try:
        results = DDGS().text(query, max_results=3)
        if not results:
            return "No results found."
        
        summary = []
        for i, res in enumerate(results, 1):
            title = res.get("title", "")
            body = res.get("body", "")
            summary.append(f"{i}. {title}: {body}")
            
        return "\n\n".join(summary)
    except Exception as e:
        return f"Error performing search: {str(e)}"
