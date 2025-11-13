"""
Finance Adapter

This adapter retrieves financial data from sources like Yahoo Finance.
Useful for stock prices, market data, company financials, and economic indicators.

TO IMPLEMENT:
1. Use yfinance library (Yahoo Finance API)
2. No API key needed for basic usage
3. Retrieve stock data, financial statements, news
4. Parse financial metrics and market data
"""

from ...domain.ports import RetrievalPort
from ...domain.models import Query, RetrievedData, Source, SourceProvider, SourceType


class FinanceAdapter(RetrievalPort):
    """
    Retrieves financial and market data.

    Example usage:
        adapter = FinanceAdapter()
        query = Query(content="AAPL stock performance")
        results = adapter.retrieve(query)
    """

    def __init__(self):
        """Initialize the Finance adapter."""
        # TODO: Initialize financial data clients
        # import yfinance as yf
        # self.yf = yf
        pass

    @property
    def provider(self) -> SourceProvider:
        """Identifies this adapter as a Finance provider."""
        return SourceProvider.FINANCE

    def retrieve(self, query: Query) -> RetrievedData:
        """
        Retrieve financial data related to the query.

        Args:
            query: The search query (e.g., stock ticker, company name)

        Returns:
            RetrievedData containing financial information
        """
        # TODO: Implement financial data retrieval logic
        #
        # Steps:
        # 1. Extract ticker symbols from the query (e.g., "AAPL", "TSLA")
        # 2. Fetch stock data, company info, and news
        # 3. Get financial metrics (P/E ratio, market cap, etc.)
        # 4. Create Source objects for each piece of information
        # 5. Include both current data and historical trends

        sources = []

        # Example implementation:
        # try:
        #     import yfinance as yf
        #     import re
        #
        #     # Try to extract ticker symbols (simple approach)
        #     # More sophisticated: use NER or keyword matching
        #     potential_tickers = re.findall(r'\b[A-Z]{1,5}\b', query.content)
        #
        #     for ticker_symbol in potential_tickers[:5]:  # Limit to 5 tickers
        #         try:
        #             ticker = yf.Ticker(ticker_symbol)
        #             info = ticker.info
        #
        #             if not info or 'regularMarketPrice' not in info:
        #                 continue  # Not a valid ticker
        #
        #             # Create source for stock overview
        #             overview = f"""
        #             {info.get('longName', ticker_symbol)} ({ticker_symbol})
        #             Current Price: ${info.get('regularMarketPrice', 'N/A')}
        #             Market Cap: ${info.get('marketCap', 'N/A'):,}
        #             P/E Ratio: {info.get('trailingPE', 'N/A')}
        #             52-Week High: ${info.get('fiftyTwoWeekHigh', 'N/A')}
        #             52-Week Low: ${info.get('fiftyTwoWeekLow', 'N/A')}
        #             """
        #
        #             source = Source(
        #                 id=f"finance_stock_{ticker_symbol}",
        #                 provider=SourceProvider.FINANCE,
        #                 type=SourceType.FINANCIAL,
        #                 url=f"https://finance.yahoo.com/quote/{ticker_symbol}",
        #                 title=f"{info.get('longName', ticker_symbol)} Stock Data",
        #                 excerpt=overview.strip(),
        #                 metadata={
        #                     'ticker': ticker_symbol,
        #                     'sector': info.get('sector'),
        #                     'industry': info.get('industry'),
        #                     'price': info.get('regularMarketPrice'),
        #                     'marketCap': info.get('marketCap'),
        #                     'pe_ratio': info.get('trailingPE'),
        #                 }
        #             )
        #             sources.append(source)
        #
        #             # Get recent news
        #             news = ticker.news[:3] if ticker.news else []
        #             for idx, article in enumerate(news):
        #                 news_source = Source(
        #                     id=f"finance_news_{ticker_symbol}_{idx}",
        #                     provider=SourceProvider.FINANCE,
        #                     type=SourceType.FINANCIAL,
        #                     url=article.get('link', ''),
        #                     title=article.get('title', 'Financial News'),
        #                     excerpt=article.get('summary', '')[:500],
        #                     metadata={
        #                         'ticker': ticker_symbol,
        #                         'publisher': article.get('publisher'),
        #                         'published': article.get('providerPublishTime'),
        #                     }
        #                 )
        #                 sources.append(news_source)
        #
        #         except Exception as e:
        #             print(f"Error fetching data for {ticker_symbol}: {e}")
        #             continue
        #
        # except Exception as e:
        #     print(f"Error retrieving financial data: {e}")

        return RetrievedData(sources=sources)


# HELPFUL RESOURCES:
# - yfinance Documentation: https://pypi.org/project/yfinance/
# - Yahoo Finance: https://finance.yahoo.com/
# - Alternative APIs: Alpha Vantage, IEX Cloud, Polygon.io
#
# TIPS:
# - yfinance is free but has rate limits
# - Extract ticker symbols carefully (avoid false positives)
# - Include both real-time and historical data
# - Handle market hours (data may be delayed outside trading hours)
# - Consider caching data to reduce API calls
# - For crypto: use different tickers (e.g., "BTC-USD")
