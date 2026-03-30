"""Utilities for filtering RSS feed entries into a clean DataFrame."""

from __future__ import annotations

import feedparser
import pandas as pd

REQUIRED_COLUMNS = ["title", "summary", "link", "published"]


def filter_rss_data(feed: feedparser.FeedParserDict) -> pd.DataFrame:
    """Return filtered RSS data with required columns and no null values.

    Raises:
        ValueError: If the feed input is invalid or required columns are missing.
    """

    _check_feed_types(feed)

    entries = feed.get("entries") if isinstance(feed, feedparser.FeedParserDict) else feed
    raw_df = pd.DataFrame(entries)

    df = _check_required_columns(raw_df)

    return df.dropna(subset=REQUIRED_COLUMNS).reset_index(drop=True)


def _check_feed_types(feed: feedparser.FeedParserDict | list) -> None:
    if isinstance(feed, list):
        return

    if not isinstance(feed, feedparser.FeedParserDict):
        raise ValueError("Invalid feed data: expected FeedParserDict or list")

    entries = feed.get("entries")
    if not isinstance(entries, list):
        raise ValueError("Invalid feed data: expected entries list")


def _check_required_columns(df: pd.DataFrame) -> None:
    missing_columns = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    if missing_columns:
        missing = ", ".join(missing_columns)
        raise ValueError(f"Missing required columns: {missing}")

    return df[REQUIRED_COLUMNS]


def _check_null_values(df: pd.DataFrame) -> None:
    if df.isnull().any().any():
        raise ValueError("Invalid feed data: null values found in required columns")