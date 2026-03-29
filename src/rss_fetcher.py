"""Utilities for fetching RSS feed entries."""

from __future__ import annotations

from typing import Any

import feedparser


class RSSFetchError(Exception):
    """Raised when an RSS feed cannot be fetched or parsed."""


def fetch_rss_feed(url: str) -> list[Any]:
    """Fetch an RSS feed URL and return feed entries."""

    feed = feedparser.parse(url)
    _handle_feed_errors(feed)

    return feed.entries


def _handle_feed_errors(feed: feedparser.FeedParserDict) -> None:
    """Handle RSS feed errors."""

    # Check for HTTP errors
    status = getattr(feed, "status", None)
    if status is not None and status >= 400:
        raise RSSFetchError(f"Failed to fetch RSS feed: HTTP {status}")

    # Check for feed parsing errors
    if getattr(feed, "bozo", 0) == 1:
        bozo_exception = getattr(feed, "bozo_exception", None)
        message = str(bozo_exception) if bozo_exception else "Invalid RSS feed"
        raise RSSFetchError(message)

    # If no errors, return and continue processing
    return
