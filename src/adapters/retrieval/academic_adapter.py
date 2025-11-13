"""
Academic Adapter

This adapter retrieves academic papers from sources like arXiv and Semantic Scholar.
Useful for research, scientific information, and technical documentation.

TO IMPLEMENT:
1. Use arXiv API and Semantic Scholar API
2. No API key needed for basic usage
3. Search for papers by keywords, authors, or topics
4. Parse paper metadata (title, abstract, authors, citations)
"""

from src.domain.ports import RetrievalPort
from src.domain.models import Query, RetrievedData, Source, SourceProvider, SourceType


class AcademicAdapter(RetrievalPort):
    """
    Retrieves academic papers from arXiv and Semantic Scholar.

    Example usage:
        adapter = AcademicAdapter()
        query = Query(content="transformer neural networks")
        results = adapter.retrieve(query)
    """

    def __init__(self, semantic_scholar_api_key: str | None = None):
        """
        Initialize the Academic adapter.

        Args:
            semantic_scholar_api_key: Optional API key for higher rate limits
        """
        self.ss_api_key = semantic_scholar_api_key

        # TODO: Initialize API clients
        # import arxiv
        # import requests
        # self.arxiv_client = arxiv.Client()
        # self.ss_base_url = "https://api.semanticscholar.org/graph/v1"

    @property
    def provider(self) -> SourceProvider:
        """Identifies this adapter as an Academic provider."""
        return SourceProvider.ACADEMIC

    def retrieve(self, query: Query) -> RetrievedData:
        """
        Retrieve academic papers related to the query.

        Args:
            query: The search query

        Returns:
            RetrievedData containing academic papers
        """
        # TODO: Implement academic search logic
        #
        # Steps:
        # 1. Search arXiv for papers
        # 2. Search Semantic Scholar for papers
        # 3. Combine and deduplicate results
        # 4. Create Source objects for each paper
        # 5. Include abstract, authors, citations, and publication date

        sources = []

        # Example implementation for arXiv:
        # try:
        #     import arxiv
        #     search = arxiv.Search(
        #         query=query.content,
        #         max_results=10,
        #         sort_by=arxiv.SortCriterion.Relevance
        #     )
        #
        #     for paper in search.results():
        #         source = Source(
        #             id=f"arxiv_{paper.entry_id.split('/')[-1]}",
        #             provider=SourceProvider.ACADEMIC,
        #             type=SourceType.ACADEMIC,
        #             url=paper.entry_id,
        #             title=paper.title,
        #             excerpt=paper.summary[:500],
        #             metadata={
        #                 'authors': [author.name for author in paper.authors],
        #                 'published': str(paper.published),
        #                 'updated': str(paper.updated),
        #                 'categories': paper.categories,
        #                 'pdf_url': paper.pdf_url,
        #             }
        #         )
        #         sources.append(source)
        #
        # except Exception as e:
        #     print(f"Error retrieving arXiv papers: {e}")

        # Example implementation for Semantic Scholar:
        # try:
        #     import requests
        #     headers = {}
        #     if self.ss_api_key:
        #         headers['x-api-key'] = self.ss_api_key
        #
        #     response = requests.get(
        #         f"{self.ss_base_url}/paper/search",
        #         params={'query': query.content, 'limit': 10},
        #         headers=headers
        #     )
        #     data = response.json()
        #
        #     for paper in data.get('data', []):
        #         source = Source(
        #             id=f"s2_{paper['paperId']}",
        #             provider=SourceProvider.ACADEMIC,
        #             type=SourceType.ACADEMIC,
        #             url=paper.get('url') or f"https://www.semanticscholar.org/paper/{paper['paperId']}",
        #             title=paper.get('title', 'Unknown'),
        #             excerpt=paper.get('abstract', '')[:500],
        #             metadata={
        #                 'authors': [a['name'] for a in paper.get('authors', [])],
        #                 'year': paper.get('year'),
        #                 'citations': paper.get('citationCount', 0),
        #                 'influentialCitations': paper.get('influentialCitationCount', 0),
        #             }
        #         )
        #         sources.append(source)
        #
        # except Exception as e:
        #     print(f"Error retrieving Semantic Scholar papers: {e}")

        return RetrievedData(sources=sources)


# HELPFUL RESOURCES:
# - arXiv API: https://arxiv.org/help/api/
# - arxiv Python package: https://pypi.org/project/arxiv/
# - Semantic Scholar API: https://api.semanticscholar.org/
# - S2 API Docs: https://api.semanticscholar.org/api-docs/
#
# TIPS:
# - arXiv is free but has rate limits (1 request/3 seconds)
# - Semantic Scholar free tier: 100 requests/5 minutes
# - Filter by citation count for influential papers
# - Check publication date for recent research
# - Some papers may not have full text available
