"""
SERP (Search Engine Results Page) Adapter

This adapter retrieves search results from search engines like Google or Bing.
It's the primary source for general web information.

TO IMPLEMENT:
1. Choose a SERP API (Google Custom Search, Bing API, SerpAPI, etc.)
2. Add API credentials to your .env file
3. Implement the retrieve() method to call the API
4. Parse the results into Source objects
5. Handle errors and rate limits
"""

from src.domain.ports import RetrievalPort
from src.domain.models import Query, RetrievedData, Source, SourceProvider, SourceType
from src.app.config import config
from tavily import TavilyClient
from pprint import pprint


class TavilySerpAdapter(RetrievalPort):
    """
    Retrieves search results from Tavily search engine.

    Example usage:
        adapter = TavilySerpAdapter() # API key is read from config
        query = Query(content="What is hexagonal architecture?")
        results = adapter.retrieve(query)
    """

    def __init__(self, api_key: str | None = None):
        """
        Initialize the SERP adapter.

        Args:
            api_key: Your search API key (get from environment variables)
        """
        self.client = TavilyClient(api_key=api_key or config.tavily_api_key)


    @property
    def provider(self) -> SourceProvider:
        """Identifies this adapter as a SERP provider."""
        return SourceProvider.SERP

    def retrieve(self, query: Query) -> RetrievedData:
        """
        Retrieve search results for the given query.

        Args:
            query: The search query from the user

        Returns:
            RetrievedData containing a list of search result sources
        """
        try:
            api_results = self.client.search(query.content)["results"]
            sources = []
            for idx, result in enumerate(api_results):
                source = Source(
                    id=f"tavily_{idx}_{hash(result['url'])}",
                    provider=SourceProvider.SERP,
                    type=SourceType.WEBPAGE,
                    url=result['url'],
                    title=result['title'],
                    excerpt=result['content'],
                    metadata={
                        'rank': idx + 1,
                        'score': result.get('score'),
                    }
                )
                sources.append(source)
        except Exception as e:
            raise RuntimeError(f"Error retrieving SERP results: {e}")

        return RetrievedData(sources=sources)

if __name__ == "__main__":
    adapter = TavilySerpAdapter()
    query = Query(content="What is hexagonal architecture?")
    results = adapter.retrieve(query)

    for source in results.sources:
        print("Source:")
        print(f"- [{source.title}]({source.url})")
        print(source)


# HELPFUL RESOURCES:
# - Google Custom Search API: https://developers.google.com/custom-search
# - Bing Search API: https://www.microsoft.com/en-us/bing/apis/bing-web-search-api
# - SerpAPI (easier, paid): https://serpapi.com/
#
# TODO 🫠:
# - Always handle rate limits and API errors
# - Cache results when possible to save API calls
# - Consider using async/await for better performance
# - Add proper logging for debugging
