# Plan: Get Data from RSS

## Overview
Implement a Python module using `feedparser` to fetch and parse medical RSS feeds (specifically Medical Xpress). The development will strictly follow TDD principles (Red, Green, Refactor).

## Phase 1: Test Development (Red Phase)
**File:** `tests/test_rss_fetcher.py`

1. **Setup Mocks:** Create a mock XML string based on the expected Medical Xpress RSS format provided in the spec.
2. **Test 1: Successful Data Fetching & Parsing**
   - **Goal:** Verify the module correctly parses RSS data and extracts the required fields.
   - **Assertion:** Ensure the returned data is a list of dictionaries where each entry contains `title`, `description`, `link`, and `pubDate`.
3. **Test 2: Error Handling (Failed Fetch)**
   - **Goal:** Verify the module handles network or parsing failures gracefully.
   - **Assertion:** Ensure a specific exception (e.g., `ConnectionError` or a custom `RSSFetchError`) is raised when given an invalid URL or when `feedparser` fails.

## Phase 2: Implementation (Green Phase)
**File:** `src/rss_fetcher.py`

1. **Function Signature:** Create `fetch_rss_feed(url: str) -> list[dict]`
2. **Fetching & Parsing logic:**
   - Use `feedparser.parse(url)` to fetch the RSS feed.
3. **Error Handling:**
   - Check if `feed.bozo` is set to `1` (which indicates a badly formatted feed or connection error) or if the `feed.status` indicates an HTTP error. Raise an exception if a failure is detected.
4. **Data Cleaning:**
   - Iterate through `feed.entries`.
   - Extract and return only the required fields: `title`, `description`, `link`, and `published` (mapped to `pubDate` in our output).

## Phase 3: Refactor & Verification
1. Run `pytest tests/test_rss_fetcher.py` to ensure all tests pass.
2. Review the code against KISS, DRY, and YAGNI principles.
3. Add proper type hinting and docstrings to the module.