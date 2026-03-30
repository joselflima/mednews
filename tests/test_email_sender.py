"""Tests for rendering and sending MedNews emails."""

from __future__ import annotations

from datetime import datetime
import smtplib
from typing import Any

import pandas as pd
import pytest

from src.email_sender import SMTPDeliveryError, build_news_email_html, send_news_email


def _sample_news_df() -> pd.DataFrame:
    """Create a sample DataFrame used by email sender tests."""

    return pd.DataFrame(
        [
            {
                "title": "Nova descoberta em cardiologia",
                "summary": "Pesquisadores identificaram um novo biomarcador.",
                "link": "https://example.com/noticia-1",
                "published": "28/03/2026",
            },
            {
                "title": "Avanços no tratamento do diabetes",
                "summary": "Estudo mostra melhora de controle glicemico.",
                "link": "https://example.com/noticia-2",
                "published": "29/03/2026",
            },
        ]
    )


def test_send_news_email_raises_when_input_is_not_dataframe() -> None:
    """Rejects invalid input types with a clear error."""

    with pytest.raises(ValueError, match="Input must be a Pandas DataFrame"):
        send_news_email([{"title": "invalid"}])


def test_build_news_email_html_contains_expected_structure() -> None:
    """Renders an HTML email body with header, news and footer."""

    news_df = _sample_news_df()
    html = build_news_email_html(news_df)
    current_date = datetime.now().strftime("%d/%m/%Y")

    assert "MedNews" in html
    assert "Seu resumo diario de noticias medicas" in html
    assert current_date in html
    assert "Nova descoberta em cardiologia" in html
    assert "Avanços no tratamento do diabetes" in html
    assert "(c) 2026 MedNews. Todos os direitos reservados." in html


def test_send_news_email_dispatches_message(monkeypatch: pytest.MonkeyPatch) -> None:
    """Sends one email message through SMTP when all inputs are valid."""

    news_df = _sample_news_df()
    monkeypatch.setenv("SMTP_SERVER", "smtp.example.com")
    monkeypatch.setenv("SMTP_PORT", "587")
    monkeypatch.setenv("SENDER_EMAIL", "sender@example.com")
    monkeypatch.setenv("SENDER_PASSWORD", "super-secret")
    monkeypatch.setenv("SUBSCRIBER_EMAIL", "subscriber@example.com")

    calls: dict[str, Any] = {"send_message": 0, "message": None}

    class MockSMTP:
        def __init__(self, *_args: Any, **_kwargs: Any) -> None:
            pass

        def __enter__(self) -> MockSMTP:
            return self

        def __exit__(self, *_args: Any) -> None:
            return None

        def starttls(self) -> None:
            return None

        def login(self, _sender: str, _password: str) -> None:
            return None

        def send_message(self, message: Any) -> None:
            calls["send_message"] += 1
            calls["message"] = message

    monkeypatch.setattr("src.email_sender.smtplib.SMTP", MockSMTP)

    send_news_email(news_df)

    assert calls["send_message"] == 1
    assert calls["message"]["To"] == "subscriber@example.com"
    payload = calls["message"].get_payload()[0].get_payload(decode=True).decode("utf-8")
    assert "Nova descoberta em cardiologia" in payload


def test_send_news_email_raises_custom_error_on_smtp_failure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Raises SMTPDeliveryError when SMTP layer fails."""

    news_df = _sample_news_df()
    monkeypatch.setenv("SMTP_SERVER", "smtp.example.com")
    monkeypatch.setenv("SMTP_PORT", "587")
    monkeypatch.setenv("SENDER_EMAIL", "sender@example.com")
    monkeypatch.setenv("SENDER_PASSWORD", "super-secret")
    monkeypatch.setenv("SUBSCRIBER_EMAIL", "subscriber@example.com")

    class FailingSMTP:
        def __init__(self, *_args: Any, **_kwargs: Any) -> None:
            pass

        def __enter__(self) -> FailingSMTP:
            return self

        def __exit__(self, *_args: Any) -> None:
            return None

        def starttls(self) -> None:
            return None

        def login(self, _sender: str, _password: str) -> None:
            return None

        def send_message(self, _message: Any) -> None:
            raise smtplib.SMTPException("SMTP failure")

    monkeypatch.setattr("src.email_sender.smtplib.SMTP", FailingSMTP)

    with pytest.raises(SMTPDeliveryError, match="Failed to send email"):
        send_news_email(news_df)


def test_send_news_email_uses_smtp_ssl_when_port_is_465(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Uses SMTP_SSL for implicit TLS providers on port 465."""

    news_df = _sample_news_df()
    monkeypatch.setenv("SMTP_SERVER", "smtp.example.com")
    monkeypatch.setenv("SMTP_PORT", "465")
    monkeypatch.setenv("SENDER_EMAIL", "sender@example.com")
    monkeypatch.setenv("SENDER_PASSWORD", "super-secret")
    monkeypatch.setenv("SUBSCRIBER_EMAIL", "subscriber@example.com")

    calls = {"ssl_used": False, "starttls_called": False}

    class MockSMTPSSL:
        def __init__(self, *_args: Any, **_kwargs: Any) -> None:
            calls["ssl_used"] = True

        def __enter__(self) -> MockSMTPSSL:
            return self

        def __exit__(self, *_args: Any) -> None:
            return None

        def login(self, _sender: str, _password: str) -> None:
            return None

        def send_message(self, _message: Any) -> None:
            return None

    class FailingSMTP:
        def __init__(self, *_args: Any, **_kwargs: Any) -> None:
            pass

        def __enter__(self) -> FailingSMTP:
            return self

        def __exit__(self, *_args: Any) -> None:
            return None

        def starttls(self) -> None:
            calls["starttls_called"] = True

        def login(self, _sender: str, _password: str) -> None:
            return None

        def send_message(self, _message: Any) -> None:
            return None

    monkeypatch.setattr("src.email_sender.smtplib.SMTP_SSL", MockSMTPSSL)
    monkeypatch.setattr("src.email_sender.smtplib.SMTP", FailingSMTP)

    send_news_email(news_df)

    assert calls["ssl_used"] is True
    assert calls["starttls_called"] is False
