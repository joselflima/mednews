# Plan: Filter RSS Data

## Overview
Implement a Python module using `pandas` to filter and structure RSS feed data. The module will accept a `FeedParserDict` object, ensure data integrity (required columns, no nulls), and output a clean pandas DataFrame. The development will strictly follow TDD principles (Red, Green, Refactor).

## Phase 1: Test Development (Red Phase)
**File:** `tests/test_filter_rss_data.py`

1. **Setup Mocks:** Create a mock `FeedParserDict` object containing a mix of valid entries, entries with missing fields, and entries with `None`/null values in required fields.
2. **Test 1: Successful Data Filtering & DataFrame Conversion**
   - **Goal:** Verify the module correctly converts the feed entries into a pandas DataFrame and selects only the required columns (`title`, `description`, `link`, `pubDate`).
   - **Assertion:** Ensure the returned object is a `pd.DataFrame` and its columns exactly match the required list.
3. **Test 2: Null Value Filtering**
   - **Goal:** Verify that rows containing null/None values in any of the required columns are dropped.
   - **Assertion:** Ensure the resulting DataFrame has no null values (`df.isnull().sum().sum() == 0`) and the row count matches the number of fully valid mock entries.
4. **Test 3: Error Handling (Missing Required Columns / Invalid Data)**
   - **Goal:** Verify the module handles completely invalid input gracefully.
   - **Assertion:** Ensure a specific exception (e.g., `ValueError` or a custom `InvalidFeedDataError`) is raised if the input data does not conform to the expected structure or is fundamentally missing required fields.

## Phase 2: Implementation (Green Phase)
**File:** `src/filter_rss_data.py`

1. **Dependencies:** Import `pandas as pd` and `feedparser` (for type hinting).
2. **Function Signature:** Create `filter_rss_data(feed: feedparser.FeedParserDict) -> pd.DataFrame`
3. **Data Extraction & Conversion:**
   - Extract the `entries` list from the `FeedParserDict`.
   - Convert the list of dictionaries into a raw pandas DataFrame (`pd.DataFrame(feed.entries)`).
4. **Validation Logic:**
   - Check if the required columns (`title`, `description`, `link`, `pubDate` / `published`) exist in the raw DataFrame. If not, raise an exception.
5. **Data Cleaning:**
   - Select only the required columns: `df[['title', 'description', 'link', 'pubDate']]`. *(Note: map 'published' to 'pubDate' if necessary based on previous module output).*
   - Apply `df.dropna(subset=['title', 'description', 'link', 'pubDate'])` to remove any rows with null values in these specific columns.
6. **Return:** Return the cleaned DataFrame.

## Phase 3: Refactor & Verification
1. Run `python -m pytest tests/test_filter_rss_data.py` to ensure all tests pass.
2. Review the code against KISS, DRY, and YAGNI principles. (e.g., ensuring we do not overcomplicate the pandas operations).
3. Ensure proper type hinting and add docstrings to the function explaining its responsibilities and potential exceptions.
