"""Utilities for building and sending MedNews emails."""

from __future__ import annotations

from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

import pandas as pd
from dotenv import load_dotenv
import os


class SMTPDeliveryError(Exception):
    """Raised when an email cannot be sent through SMTP."""


def build_news_email_html(news_df: pd.DataFrame) -> str:
    """Build the responsive HTML body for the daily MedNews email."""

    current_date = datetime.now().strftime("%d/%m/%Y")
    news_items_html = ""

    for _, row in news_df.iterrows():
        news_items_html += f"""
        <tr>
          <td style="padding: 0 24px 0 24px;">
            <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="border-collapse: collapse;">
              <tr>
                <td style="padding: 18px 0 8px 0; font-family: 'Trebuchet MS', Helvetica, sans-serif; color: #1f2a44; font-size: 22px; line-height: 1.3; font-weight: 700;">{row['title']}</td>
              </tr>
              <tr>
                <td style="padding: 0 0 10px 0; font-family: 'Trebuchet MS', Helvetica, sans-serif; color: #5a6478; font-size: 14px; line-height: 1.4;">Publicado em: {row['published']}</td>
              </tr>
              <tr>
                <td style="padding: 0 0 14px 0; font-family: Georgia, 'Times New Roman', serif; color: #2f3542; font-size: 16px; line-height: 1.6;">{row['summary']}</td>
              </tr>
              <tr>
                <td style="padding: 0 0 18px 0;">
                  <a href="{row['link']}" style="display: inline-block; background-color: #1a73e8; color: #ffffff; font-family: 'Trebuchet MS', Helvetica, sans-serif; font-size: 14px; text-decoration: none; padding: 10px 16px; border-radius: 8px;">Ler noticia completa</a>
                </td>
              </tr>
              <tr>
                <td style="height: 1px; border-top: 1px solid #dde3ec; font-size: 0; line-height: 0;">&nbsp;</td>
              </tr>
              <tr>
                <td style="height: 14px; font-size: 0; line-height: 0;">&nbsp;</td>
              </tr>
            </table>
          </td>
        </tr>
        """

    return f"""
    <!DOCTYPE html>
    <html lang="pt-BR">
      <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>MedNews</title>
      </head>
      <body style="margin: 0; padding: 0; background: linear-gradient(135deg, #f5f8ff 0%, #eef7f3 100%);">
        <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="border-collapse: collapse; width: 100%;">
          <tr>
            <td align="center" style="padding: 24px 12px;">
              <table role="presentation" width="640" cellspacing="0" cellpadding="0" border="0" style="border-collapse: collapse; width: 100%; max-width: 640px; background-color: #ffffff; border-radius: 16px; overflow: hidden;">
                <tr>
                  <td style="padding: 28px 24px; background: linear-gradient(120deg, #1f3b73 0%, #2879c9 100%);">
                    <h1 style="margin: 0; font-family: 'Trebuchet MS', Helvetica, sans-serif; color: #ffffff; font-size: 34px; line-height: 1.2;">MedNews</h1>
                    <p style="margin: 8px 0 0 0; font-family: 'Trebuchet MS', Helvetica, sans-serif; color: #dbe9ff; font-size: 16px;">Seu resumo diario de noticias medicas</p>
                    <p style="margin: 16px 0 0 0; font-family: 'Trebuchet MS', Helvetica, sans-serif; color: #b8d5ff; font-size: 13px;">{current_date}</p>
                  </td>
                </tr>
                {news_items_html}
                <tr>
                  <td style="padding: 18px 24px; text-align: center; background-color: #f2f5fa; font-family: 'Trebuchet MS', Helvetica, sans-serif; color: #7f8c8d; font-size: 12px; line-height: 1.5;">
                    <div style="font-size: 13px;">MedNews - {current_date}</div>
                    <div style="margin-top: 4px;">(c) 2026 MedNews. Todos os direitos reservados.</div>
                  </td>
                </tr>
              </table>
            </td>
          </tr>
        </table>
      </body>
    </html>
    """


def send_news_email(news_df: pd.DataFrame) -> None:
    """Send daily translated news to the configured subscriber."""

    if not isinstance(news_df, pd.DataFrame):
        raise ValueError("Input must be a Pandas DataFrame")

    load_dotenv()

    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD")
    subscriber_email = os.getenv("SUBSCRIBER_EMAIL")

    if not smtp_server:
        raise SMTPDeliveryError("Missing SMTP_SERVER environment variable")
    if not sender_email:
        raise SMTPDeliveryError("Missing SENDER_EMAIL environment variable")
    if not sender_password:
        raise SMTPDeliveryError("Missing SENDER_PASSWORD environment variable")
    if not subscriber_email:
        raise SMTPDeliveryError("Missing SUBSCRIBER_EMAIL environment variable")

    message = MIMEMultipart("alternative")
    message["Subject"] = "MedNews - Seu resumo diario de noticias medicas"
    message["From"] = sender_email
    message["To"] = subscriber_email
    message.attach(MIMEText(build_news_email_html(news_df), "html", "utf-8"))

    try:
        if smtp_port == 465:
            smtp_client = smtplib.SMTP_SSL(smtp_server, smtp_port)
        else:
            smtp_client = smtplib.SMTP(smtp_server, smtp_port)

        with smtp_client as smtp:
            if smtp_port != 465:
                smtp.starttls()
            smtp.login(sender_email, sender_password)
            smtp.send_message(message)
    except (smtplib.SMTPException, OSError) as exc:
        raise SMTPDeliveryError("Failed to send email") from exc
