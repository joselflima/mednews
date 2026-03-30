# Tasks: Translate Title and Subtitle

## 1. Setup & Configuration
- [x] Verify `pandas` and `groq` are in `requirements.txt` and install them if necessary.
- [x] Ensure `python-dotenv` is configured to load `GROQ_API_KEY`.

## 2. Tests Implementation (TDD - Red Phase)
- [x] Create test file `tests/test_translator.py`.
- [x] **Test 1:** Input Validation - Success (DataFrame has `title`, `summary`, `link`, `published`).
- [x] **Test 2:** Input Validation - Missing Columns (Throws exception if `title` or `summary` are missing).
- [x] **Test 3:** Input Validation - Null Values (Throws exception if `title` or `summary` are null).
- [x] **Test 4:** LLM Output Validation - JSON Parse (Mock API to return malformed JSON, verify exception is thrown).
- [x] **Test 5:** LLM Output Validation - Missing Keys (Mock API to return valid JSON without `title` or `description` keys, verify exception is thrown).
- [x] **Test 6:** Happy Path (Mock successful API response, verify DataFrame is updated with translated fields).

## 3. Module Implementation (TDD - Green Phase)
- [x] Create module file `src/translator.py`.
- [x] Implement `validate_input(df: pd.DataFrame)` to check for required columns and null values.
- [x] Implement `call_groq_api(title: str, summary: str) -> dict` to call Groq API (`gemma-7b`) and handle connection/rate limit errors.
- [x] Implement `parse_llm_response(response_text: str) -> dict` to parse JSON and validate required keys (`title`, `description`).
- [x] Implement `translate_feed(df: pd.DataFrame) -> pd.DataFrame` to orchestrate the translation process row by row.

## 4. Refactoring (TDD - Refactor Phase)
- [x] Review implementation for KISS, DRY, and YAGNI principles.
- [x] Ensure all mock data in tests properly isolated from real API calls.
- [x] Run `pytest tests/test_translator.py` and ensure all tests pass.
