"""
Reddit Adapter

This adapter retrieves posts and comments from Reddit.
Useful for gathering community opinions, discussions, and recent trends.

TO IMPLEMENT:
1. Use PRAW (Python Reddit API Wrapper) or Reddit API
2. Add Reddit API credentials to your .env file
3. Implement search across relevant subreddits
4. Parse posts and top comments into Source objects
"""

from src.domain.ports import RetrievalPort
from src.domain.models import Query, RetrievedData, Source, SourceProvider, SourceType


class RedditAdapter(RetrievalPort):
    """
    Retrieves posts and discussions from Reddit.

    Example usage:
        adapter = RedditAdapter(
            client_id="your_id",
            client_secret="your_secret",
            user_agent="your_app_name"
        )
        query = Query(content="Python best practices")
        results = adapter.retrieve(query)
    """

    def __init__(
        self,
        client_id: str | None = None,
        client_secret: str | None = None,
        user_agent: str = "TeraFinder/0.1"
    ):
        """
        Initialize the Reddit adapter.

        Args:
            client_id: Reddit API client ID
            client_secret: Reddit API client secret
            user_agent: User agent string for API requests
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.user_agent = user_agent

        # TODO: Initialize PRAW client
        # import praw
        # self.reddit = praw.Reddit(
        #     client_id=self.client_id,
        #     client_secret=self.client_secret,
        #     user_agent=self.user_agent
        # )

    @property
    def provider(self) -> SourceProvider:
        """Identifies this adapter as a Reddit provider."""
        return SourceProvider.REDDIT

    def retrieve(self, query: Query) -> RetrievedData:
        """
        Retrieve Reddit posts related to the query.

        Args:
            query: The search query

        Returns:
            RetrievedData containing Reddit posts and top comments
        """
        # TODO: Implement Reddit search logic
        #
        # Steps:
        # 1. Search across relevant subreddits or all of Reddit
        # 2. Filter by relevance, score, or time
        # 3. For each post, optionally get top comments
        # 4. Create Source objects for posts (and comments)
        # 5. Return RetrievedData

        sources = []

        # Example implementation:
        # try:
        #     # Search Reddit (can search specific subreddits or all)
        #     subreddit = self.reddit.subreddit("all")
        #     posts = subreddit.search(query.content, limit=10, sort="relevance")
        #
        #     for post in posts:
        #         # Create source for the post
        #         source = Source(
        #             id=f"reddit_post_{post.id}",
        #             provider=SourceProvider.REDDIT,
        #             type=SourceType.SOCIAL,
        #             url=f"https://reddit.com{post.permalink}",
        #             title=post.title,
        #             excerpt=post.selftext[:500] if post.selftext else post.title,
        #             metadata={
        #                 'score': post.score,
        #                 'num_comments': post.num_comments,
        #                 'subreddit': post.subreddit.display_name,
        #                 'author': str(post.author),
        #                 'created_utc': post.created_utc,
        #             }
        #         )
        #         sources.append(source)
        #
        #         # Optionally, get top comments
        #         post.comment_sort = "top"
        #         post.comments.replace_more(limit=0)  # Remove "load more"
        #         for comment in post.comments[:3]:  # Top 3 comments
        #             comment_source = Source(
        #                 id=f"reddit_comment_{comment.id}",
        #                 provider=SourceProvider.REDDIT,
        #                 type=SourceType.SOCIAL,
        #                 url=f"https://reddit.com{post.permalink}{comment.id}",
        #                 title=f"Comment on: {post.title}",
        #                 excerpt=comment.body[:500],
        #                 metadata={
        #                     'score': comment.score,
        #                     'author': str(comment.author),
        #                     'parent_post_id': post.id,
        #                 }
        #             )
        #             sources.append(comment_source)
        #
        # except Exception as e:
        #     print(f"Error retrieving Reddit data: {e}")

        return RetrievedData(sources=sources)


# HELPFUL RESOURCES:
# - PRAW Documentation: https://praw.readthedocs.io/
# - Reddit API: https://www.reddit.com/dev/api/
# - Get API credentials: https://www.reddit.com/prefs/apps
#
# TIPS:
# - Respect Reddit's API rate limits (60 requests per minute)
# - Filter by subreddit relevance for better results
# - Consider post score and comment count for quality
# - Handle deleted posts and shadowbanned users gracefully
