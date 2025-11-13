"""
Twitter (X) Adapter

This adapter retrieves posts (tweets) from X (formerly Twitter).
Useful for real-time information, trending topics, and public opinion.

TO IMPLEMENT:
1. Use tweepy library or X API v2
2. Add X API credentials to your .env file (API key, bearer token)
3. Implement search for recent tweets
4. Handle rate limits and authentication
"""

from src.domain.ports import RetrievalPort
from src.domain.models import Query, RetrievedData, Source, SourceProvider, SourceType


class TwitterAdapter(RetrievalPort):
    """
    Retrieves tweets from X (Twitter).

    Example usage:
        adapter = TwitterAdapter(bearer_token="your_token")
        query = Query(content="artificial intelligence")
        results = adapter.retrieve(query)
    """

    def __init__(self, bearer_token: str | None = None):
        """
        Initialize the Twitter adapter.

        Args:
            bearer_token: X API bearer token (v2 API)
        """
        self.bearer_token = bearer_token

        # TODO: Initialize Twitter API client
        # import tweepy
        # self.client = tweepy.Client(bearer_token=self.bearer_token)

    @property
    def provider(self) -> SourceProvider:
        """Identifies this adapter as a Twitter provider."""
        return SourceProvider.TWITTER

    def retrieve(self, query: Query) -> RetrievedData:
        """
        Retrieve tweets related to the query.

        Args:
            query: The search query

        Returns:
            RetrievedData containing tweets
        """
        # TODO: Implement Twitter search logic
        #
        # Steps:
        # 1. Search for recent tweets using the query
        # 2. Filter by relevance, retweets, or likes
        # 3. Get tweet metadata (author, timestamp, engagement)
        # 4. Create Source objects for each tweet
        # 5. Handle pagination if needed

        sources = []

        # Example implementation:
        # try:
        #     # Search recent tweets (last 7 days with free tier)
        #     tweets = self.client.search_recent_tweets(
        #         query=query.content,
        #         max_results=100,  # Max 100 per request
        #         tweet_fields=['created_at', 'public_metrics', 'author_id'],
        #         expansions=['author_id'],
        #         user_fields=['username', 'name']
        #     )
        #
        #     if not tweets.data:
        #         return RetrievedData(sources=[])
        #
        #     # Create a user lookup for author info
        #     users = {user.id: user for user in tweets.includes['users']}
        #
        #     for tweet in tweets.data:
        #         author = users.get(tweet.author_id)
        #         metrics = tweet.public_metrics
        #
        #         source = Source(
        #             id=f"twitter_{tweet.id}",
        #             provider=SourceProvider.TWITTER,
        #             type=SourceType.SOCIAL,
        #             url=f"https://twitter.com/{author.username}/status/{tweet.id}",
        #             title=f"Tweet by @{author.username}",
        #             excerpt=tweet.text,
        #             metadata={
        #                 'author': author.name,
        #                 'username': author.username,
        #                 'created_at': str(tweet.created_at),
        #                 'retweets': metrics['retweet_count'],
        #                 'likes': metrics['like_count'],
        #                 'replies': metrics['reply_count'],
        #             }
        #         )
        #         sources.append(source)
        #
        # except Exception as e:
        #     print(f"Error retrieving Twitter data: {e}")

        return RetrievedData(sources=sources)


# HELPFUL RESOURCES:
# - Tweepy Documentation: https://docs.tweepy.org/
# - X API v2: https://developer.twitter.com/en/docs/twitter-api
# - Get API credentials: https://developer.twitter.com/en/portal/dashboard
#
# TIPS:
# - Free tier only allows recent tweets (last 7 days)
# - Rate limits: 450 requests per 15 minutes (app auth)
# - Use tweet engagement metrics to filter quality content
# - Consider filtering out retweets: add -is:retweet to query
# - Handle different tweet types: replies, quotes, retweets
