"""Utilities for translating RSS title and summary fields."""

from __future__ import annotations

import json
import time

import groq
import pandas as pd
from groq import Groq

REQUIRED_COLUMNS = ["title", "summary", "link", "published"]
TRANSLATED_KEYS = ["title", "summary"]


def validate_input(df: pd.DataFrame) -> pd.DataFrame:
    """Validate DataFrame input and return required columns."""

    if not isinstance(df, pd.DataFrame):
        raise ValueError("Invalid input: expected a pandas DataFrame")

    missing_columns = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    if missing_columns:
        missing = ", ".join(missing_columns)
        raise ValueError(f"Missing required columns: {missing}")

    required_df = df[REQUIRED_COLUMNS].copy()
    if required_df[["title", "summary"]].isnull().any().any():
        raise ValueError("Invalid input: null values found in title or summary")

    return required_df


def call_groq_api(title: str, summary: str) -> str:
    """Call Groq API and return raw model text response."""

    client = Groq()
    payload = json.dumps({"title": title, "summary": summary})

    try:
        completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a translator from English to Portuguese. "
                        "Answer only a JSON object with keys 'title' and 'summary'."
                    ),
                },
                {"role": "user", "content": payload},
            ],
            model="llama-3.1-8b-instant",
            temperature=0.1,
        )
    except groq.APIConnectionError as exc:
        raise RuntimeError("Groq API connection error") from exc
    except groq.RateLimitError as exc:
        raise RuntimeError("Groq API rate limit exceeded") from exc
    except groq.APIStatusError as exc:
        raise RuntimeError(f"Groq API status error: {exc.status_code}") from exc

    content = completion.choices[0].message.content
    if not isinstance(content, str) or not content.strip():
        raise ValueError("Groq API returned an empty response")

    return content


def parse_llm_response(response_text: str) -> dict[str, str]:
    """Parse and validate LLM JSON response."""

    try:
        parsed = json.loads(response_text)
    except json.JSONDecodeError as exc:
        raise ValueError("LLM response must be valid JSON") from exc

    if not isinstance(parsed, dict):
        raise ValueError("LLM response must be a JSON object")

    if not all(key in parsed for key in TRANSLATED_KEYS):
        raise ValueError("LLM response must contain 'title' and 'summary'")

    return {
        "title": str(parsed["title"]),
        "summary": str(parsed["summary"]),
    }


def translate_feed(df: pd.DataFrame) -> pd.DataFrame:
    """Translate title and summary columns to Portuguese row by row."""

    translated_df = validate_input(df)

    rows = list(translated_df.iterrows())
    for i, (index, row) in enumerate(rows):
        response_text = call_groq_api(row["title"], row["summary"])
        translated = parse_llm_response(response_text)

        translated_df.at[index, "title"] = translated["title"]
        translated_df.at[index, "summary"] = translated["summary"]

        if i < len(rows) - 1:
            time.sleep(1)

    return translated_df
