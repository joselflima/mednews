"""Tests for translating RSS title and summary fields."""

from __future__ import annotations

import json
import time

import pandas as pd
import pytest

from src.translator import translate_feed


def _build_feed_dataframe() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "title": "Original title",
                "summary": "Original summary",
                "link": "https://example.com/news",
                "published": "Fri, 28 Mar 2026 10:00:00 GMT",
            }
        ]
    )


def test_translate_feed_accepts_dataframe_with_required_columns(monkeypatch: pytest.MonkeyPatch) -> None:
    """Accepts a valid DataFrame input and returns translated content."""

    def mock_call_groq_api(_: str, __: str) -> str:
        return json.dumps({"title": "Titulo", "summary": "Resumo"})

    monkeypatch.setattr("src.translator.call_groq_api", mock_call_groq_api)

    result = translate_feed(_build_feed_dataframe())

    assert isinstance(result, pd.DataFrame)
    assert list(result.columns) == ["title", "summary", "link", "published"]


def test_translate_feed_raises_for_missing_required_columns() -> None:
    """Raises an exception when title or summary columns are missing."""

    invalid_df = pd.DataFrame([{"link": "https://example.com", "published": "today"}])

    with pytest.raises(ValueError, match="Missing required columns"):
        translate_feed(invalid_df)


def test_translate_feed_raises_for_null_title_or_summary() -> None:
    """Raises an exception when title or summary has null values."""

    invalid_df = pd.DataFrame(
        [
            {
                "title": None,
                "summary": "Some summary",
                "link": "https://example.com/news",
                "published": "Fri, 28 Mar 2026 10:00:00 GMT",
            }
        ]
    )

    with pytest.raises(ValueError, match="null values"):
        translate_feed(invalid_df)


def test_translate_feed_raises_when_llm_response_is_not_valid_json(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Raises an exception when LLM response cannot be parsed as JSON."""

    def mock_call_groq_api(_: str, __: str) -> str:
        return "not-a-json"

    monkeypatch.setattr("src.translator.call_groq_api", mock_call_groq_api)

    with pytest.raises(ValueError, match="valid JSON"):
        translate_feed(_build_feed_dataframe())


def test_translate_feed_raises_when_llm_response_missing_required_keys(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Raises an exception when translated keys are not present."""

    def mock_call_groq_api(_: str, __: str) -> str:
        return json.dumps({"title": "Titulo"})

    monkeypatch.setattr("src.translator.call_groq_api", mock_call_groq_api)

    with pytest.raises(ValueError, match="must contain 'title' and 'summary'"):
        translate_feed(_build_feed_dataframe())


def test_translate_feed_returns_dataframe_with_translated_columns(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Returns DataFrame with translated title and summary values."""

    def mock_call_groq_api(title: str, summary: str) -> str:
        assert title == "Original title"
        assert summary == "Original summary"
        return json.dumps(
            {
                "title": "Titulo traduzido",
                "summary": "Resumo traduzido",
            }
        )

    monkeypatch.setattr("src.translator.call_groq_api", mock_call_groq_api)

    result = translate_feed(_build_feed_dataframe())

    assert len(result) == 1
    assert result.loc[0, "title"] == "Titulo traduzido"
    assert result.loc[0, "summary"] == "Resumo traduzido"


def test_translate_feed_waits_one_second_between_rows(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Calls time.sleep(1) between each row to avoid Groq API rate limits."""

    sleep_calls: list[float] = []

    def mock_sleep(seconds: float) -> None:
        sleep_calls.append(seconds)

    def mock_call_groq_api(_: str, __: str) -> str:
        return json.dumps({"title": "Titulo", "summary": "Resumo"})

    import src.translator as translator_module

    monkeypatch.setattr(translator_module.time, "sleep", mock_sleep)
    monkeypatch.setattr("src.translator.call_groq_api", mock_call_groq_api)

    multi_row_df = pd.DataFrame(
        [
            {
                "title": "Title 1",
                "summary": "Summary 1",
                "link": "https://example.com/1",
                "published": "Fri, 28 Mar 2026 10:00:00 GMT",
            },
            {
                "title": "Title 2",
                "summary": "Summary 2",
                "link": "https://example.com/2",
                "published": "Fri, 28 Mar 2026 11:00:00 GMT",
            },
            {
                "title": "Title 3",
                "summary": "Summary 3",
                "link": "https://example.com/3",
                "published": "Fri, 28 Mar 2026 12:00:00 GMT",
            },
        ]
    )

    translate_feed(multi_row_df)

    # sleep should be called once BETWEEN rows: n_rows - 1 times
    assert sleep_calls == [1, 1]
