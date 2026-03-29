# Tasks: Get Data from RSS

## Phase 1: Preparation & Test Development (Red Phase)
- [v] Create test file `tests/test_rss_fetcher.py`.
- [v] Create a mock XML string based on the Medical Xpress RSS format for testing.
- [v] Write **Test 1 (Success)**: Verify that the module correctly parses the mocked RSS data and returns a list of dictionaries containing strictly the fields: `title`, `description`, `link`, and `pubDate`.
- [v] Write **Test 2 (Failure)**: Verify that the module gracefully handles network errors or invalid URLs by throwing a specific exception (e.g., `ConnectionError` or custom `RSSFetchError`).
- [v] Run `pytest` to confirm that the tests fail (Red phase).

## Phase 2: Implementation (Green Phase)
- [v] Create source file `src/rss_fetcher.py`.
- [v] Implement the function `fetch_rss_feed(url: str) -> list[dict]`.
- [v] Add fetching logic using the `feedparser` library.
- [v] Add error handling logic: raise an exception if the fetch fails (e.g., checking `feed.bozo == 1` or checking HTTP status).
- [v] Run `pytest` to ensure all tests now pass (Green phase).

## Phase 3: Refactor & Verification
- [v] Review the implementation against KISS, DRY, and YAGNI principles.
- [v] Add proper type hinting to the `fetch_rss_feed` function.
- [v] Add docstrings explaining the module and function.
- [v] Run the final test suite to ensure no regressions were introduced during refactoring.