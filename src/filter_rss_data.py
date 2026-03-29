"""Utilities for filtering RSS feed entries into a clean DataFrame."""

from __future__ import annotations

import feedparser
import pandas as pd

REQUIRED_COLUMNS = ["title", "description", "link", "pubDate"]


def filter_rss_data(feed: feedparser.FeedParserDict) -> pd.DataFrame:
    """Return filtered RSS data with required columns and no null values.

    Raises:
        ValueError: If the feed input is invalid or required columns are missing.
    """

    _check_feed_types(feed)

    raw_df = pd.DataFrame(feed.get("entries"))

    if "pubDate" not in raw_df.columns and "published" in raw_df.columns:
        raw_df["pubDate"] = raw_df["published"]

    df = _check_required_columns(raw_df)

    return df.dropna(subset=REQUIRED_COLUMNS).reset_index(drop=True)


def _check_feed_types(feed: feedparser.FeedParserDict) -> None:
    if not isinstance(feed, feedparser.FeedParserDict):
        raise ValueError("Invalid feed data: expected FeedParserDict")

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