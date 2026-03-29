"""Tests for filtering and structuring RSS feed data."""

import feedparser
import pandas as pd
import pytest

from src.filter_rss_data import filter_rss_data


def test_filter_rss_data_returns_dataframe_with_required_columns() -> None:
    """Returns a DataFrame containing only required columns."""

    feed = feedparser.FeedParserDict(
        {
            "entries": [
                {
                    "title": "Headline 1",
                    "description": "Description 1",
                    "link": "https://example.com/1",
                    "published": "Fri, 28 Mar 2026 10:00:00 GMT",
                    "category": "Health",
                },
                {
                    "title": "Headline 2",
                    "description": "Description 2",
                    "link": "https://example.com/2",
                    "pubDate": "Fri, 28 Mar 2026 11:00:00 GMT",
                    "author": "Someone",
                },
            ]
        }
    )

    result = filter_rss_data(feed)

    assert isinstance(result, pd.DataFrame)
    assert list(result.columns) == ["title", "description", "link", "pubDate"]


def test_filter_rss_data_removes_rows_with_null_values() -> None:
    """Drops rows with null values in any required field."""

    feed = feedparser.FeedParserDict(
        {
            "entries": [
                {
                    "title": "Valid headline",
                    "description": "Valid description",
                    "link": "https://example.com/valid",
                    "pubDate": "Fri, 28 Mar 2026 10:00:00 GMT",
                },
                {
                    "title": "Invalid headline",
                    "description": None,
                    "link": "https://example.com/invalid",
                    "pubDate": "Fri, 28 Mar 2026 11:00:00 GMT",
                },
            ]
        }
    )

    result = filter_rss_data(feed)

    assert len(result) == 1
    assert result.isnull().sum().sum() == 0


def test_filter_rss_data_raises_exception_for_invalid_feed_data() -> None:
    """Raises ValueError when required columns are missing."""

    feed = feedparser.FeedParserDict(
        {
            "entries": [
                {
                    "title": "Headline only",
                    "link": "https://example.com/1",
                }
            ]
        }
    )

    with pytest.raises(ValueError, match="Missing required columns"):
        filter_rss_data(feed)
