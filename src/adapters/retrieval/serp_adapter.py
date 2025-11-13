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


class SerpAdapter(RetrievalPort):
    """
    Retrieves search results from search engines.

    Example usage:
        adapter = SerpAdapter(api_key="your_key")
        query = Query(content="What is hexagonal architecture?")
        results = adapter.retrieve(query)
    """

    def __init__(self, api_key: str | None = None):
        """
        Initialize the SERP adapter.

        Args:
            api_key: Your search API key (get from environment variables)
        """
        self.api_key = api_key
        # TODO: Initialize your search API client here
        # Example: self.client = GoogleSearchClient(api_key=self.api_key)

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
        # TODO: Implement the actual search logic
        #
        # Steps:
        # 1. Call your search API with query.content
        # 2. Get the results (usually top 10-20 results)
        # 3. For each result, create a Source object
        # 4. Return RetrievedData with all sources

        # Placeholder implementation:
        sources = []

        # Example of what you should do:
        # try:
        #     api_results = self.client.search(query.content, num_results=10)
        #
        #     for idx, result in enumerate(api_results):
        #         source = Source(
        #             id=f"serp_{idx}_{hash(result['url'])}",
        #             provider=SourceProvider.SERP,
        #             type=SourceType.WEBPAGE,
        #             url=result['url'],
        #             title=result['title'],
        #             excerpt=result['snippet'],
        #             metadata={
        #                 'rank': idx + 1,
        #                 'timestamp': result.get('date'),
        #             }
        #         )
        #         sources.append(source)
        #
        # except Exception as e:
        #     # Handle errors gracefully
        #     print(f"Error retrieving SERP results: {e}")
        #     # You might want to log this or raise a custom exception

        return RetrievedData(sources=sources)


# HELPFUL RESOURCES:
# - Google Custom Search API: https://developers.google.com/custom-search
# - Bing Search API: https://www.microsoft.com/en-us/bing/apis/bing-web-search-api
# - SerpAPI (easier, paid): https://serpapi.com/
#
# TIPS:
# - Always handle rate limits and API errors
# - Cache results when possible to save API calls
# - Consider using async/await for better performance
# - Add proper logging for debugging
