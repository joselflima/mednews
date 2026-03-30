"""Tests for MedNews pipeline orchestration in main module."""

from __future__ import annotations

import pandas as pd

from src.main import main


def test_main_calls_email_sender_with_translated_dataframe(
    monkeypatch,
) -> None:
    """Ensures pipeline sends translated dataframe by email."""

    called: dict[str, pd.DataFrame | None] = {"sent_df": None}
    translated_df = pd.DataFrame(
        [
            {
                "title": "Titulo traduzido",
                "summary": "Resumo traduzido",
                "link": "https://example.com/noticia",
                "published": "29/03/2026",
            }
        ]
    )

    monkeypatch.setattr("src.main.fetch_rss_feed", lambda _url: [{"title": "raw"}])
    monkeypatch.setattr("src.main.filter_rss_data", lambda _feed: pd.DataFrame())
    monkeypatch.setattr("src.main.translate_feed", lambda _df: translated_df)

    def _mock_send_news_email(df: pd.DataFrame) -> None:
        called["sent_df"] = df

    monkeypatch.setattr("src.main.send_news_email", _mock_send_news_email)

    main()

    assert called["sent_df"] is not None
    assert called["sent_df"].equals(translated_df)
