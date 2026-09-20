from app.tools.base import BaseTool


class SearchTool(BaseTool):
    """Web search tool (placeholder).

    TODO: Integrate a real search provider:
    - SerpAPI: pip install google-search-results
    - Tavily: pip install tavily-python
    - DuckDuckGo: pip install duckduckgo-search

    Example integration:
        from tavily import TavilyClient
        client = TavilyClient(api_key=settings.TAVILY_API_KEY)
        results = client.search(query, max_results=5)
        return results["results"]
    """

    @property
    def name(self) -> str:
        return "search"

    @property
    def description(self) -> str:
        return (
            "Searches the web for information. Input should be a search query string."
        )

    def execute(self, query: str = "", **kwargs) -> list[dict]:
        """Perform a web search.

        TODO: Replace with real search API call.
        """
        # Mock results for testing
        return [
            {
                "title": f"Mock Result 1 for '{query}'",
                "url": "https://example.com/1",
                "snippet": f"This is a placeholder result for the query: {query}",
            },
            {
                "title": f"Mock Result 2 for '{query}'",
                "url": "https://example.com/2",
                "snippet": "Another placeholder result with mock information.",
            },
            {
                "title": f"Mock Result 3 for '{query}'",
                "url": "https://example.com/3",
                "snippet": "Third mock result for testing the agent pipeline.",
            },
        ]
