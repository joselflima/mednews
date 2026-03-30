# Plan: Translate Title and Subtitle

## 1. Overview
Implement a new module to translate the `title` and `summary` columns of a pandas DataFrame from English to Portuguese using the Groq API (Gemma 7B model). The development will follow TDD (Red, Green, Refactor) principles.

## 2. Dependencies and Setup
- Ensure `pandas` and `groq` are installed and added to `requirements.txt`.
- Ensure `pytest` is configured to run tests for the new module.
- Set up `python-dotenv` to load the `GROQ_API_KEY` environment variable.

## 3. Testing Strategy (TDD - Write Tests First)
Create a new test file `tests/test_translator.py`.

### Test Cases to Implement:
1. **Input Validation - Success:** Test that the module correctly accepts a DataFrame with `title`, `summary`, `link`, and `published` columns.
2. **Input Validation - Missing Columns:** Test that an exception is raised if the input DataFrame lacks `title` or `summary` columns.
3. **Input Validation - Null Values:** Test that an exception is raised or handled appropriately if `title` or `summary` contains null values.
4. **LLM Output Validation - JSON Parse:** Mock the Groq API to return a malformed JSON string and test that the module throws a specific exception.
5. **LLM Output Validation - Missing Keys:** Mock the Groq API to return valid JSON but without the `title` or `description` keys, and verify it throws an exception.
6. **Happy Path:** Mock a successful Groq API JSON response. Test that the module correctly translates the fields, updates the row, and returns the modified DataFrame.

## 4. Implementation Steps
Create the module `src/translator.py`.

### Functions:
- `validate_input(df: pd.DataFrame)`: Checks for required columns (`title`, `summary`, `link`, `published`) and ensures `title` and `summary` are not null.
- `call_groq_api(title: str, summary: str) -> dict`: Calls the Groq API using `gemma-7b`. Handles API errors (Connection, RateLimit, Status).
- `parse_llm_response(response_text: str) -> dict`: Parses the JSON string from the API and validates `title` and `description` keys.
- `translate_feed(df: pd.DataFrame) -> pd.DataFrame`: Main entry point. Orchestrates validation and translation for each row.

## 5. Refactoring
- Ensure code follows KISS, DRY, and YAGNI principles.
- Use mocks for Groq API calls in tests to avoid actual API usage and costs during development.
- Ensure error messages are clear and helpful.
