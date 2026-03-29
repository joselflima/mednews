"""Tests for RSS feed fetching and parsing."""

from types import SimpleNamespace

import feedparser
import pytest

from src.rss_fetcher import RSSFetchError, fetch_rss_feed


MOCK_MEDICAL_XPRESS_RSS = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>Medical Xpress - latest news</title>
    <item>
      <title>First medical headline</title>
      <description>First description from Medical Xpress.</description>
      <link>https://medicalxpress.com/news/first.html</link>
      <pubDate>Fri, 28 Mar 2026 10:00:00 GMT</pubDate>
    </item>
    <item>
      <title>Second medical headline</title>
      <description>Second description from Medical Xpress.</description>
      <link>https://medicalxpress.com/news/second.html</link>
      <pubDate>Fri, 28 Mar 2026 11:00:00 GMT</pubDate>
    </item>
  </channel>
</rss>
"""


def test_fetch_rss_feed_returns_entries_successfully(monkeypatch: pytest.MonkeyPatch) -> None:
    """Parses mocked RSS and returns entries from the feed."""

    parsed_feed = feedparser.parse(MOCK_MEDICAL_XPRESS_RSS)

    def mock_parse(_: str):
      return parsed_feed

    monkeypatch.setattr("src.rss_fetcher.feedparser.parse", mock_parse)

    result = fetch_rss_feed("https://medicalxpress.com/rss-feed")

    assert isinstance(result, list)
    assert len(result) == len(parsed_feed.entries)

    # Check that entries have expected data from mock
    for item in result:
      assert "title" in item
      assert isinstance(item["title"], str)


def test_fetch_rss_feed_raises_rss_fetch_error_on_invalid_feed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Raises a specific exception when feed parsing indicates an error."""

    invalid_feed = SimpleNamespace(
        bozo=1,
        bozo_exception=ConnectionError("Invalid URL or network failure"),
    )

    def mock_parse(_: str):
        return invalid_feed

    monkeypatch.setattr("src.rss_fetcher.feedparser.parse", mock_parse)

    with pytest.raises(RSSFetchError, match="Invalid URL or network failure"):
        fetch_rss_feed("invalid-url")
