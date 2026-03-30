# Plan: Send News via Email

## Overview
Implement a Python module to send translated medical news to a subscriber via email. The module should accept a Pandas DataFrame containing `title`, `summary`, `link`, and `published` news data, and send a beautifully styled HTML email using `smtplib`. The development will strictly follow TDD principles (Red, Green, Refactor).

## Phase 1: Test Development (Red Phase)
**File:** `tests/test_email_sender.py`

1. **Setup Mocks:**
   - Mock `smtplib.SMTP` and `smtplib.SMTP_SSL` to prevent actual network calls.
   - Mock `pandas.DataFrame` for input data.
2. **Test 1: Input Validation**
   - **Goal:** Ensure the module only accepts a Pandas DataFrame.
   - **Assertion:** `pytest.raises(ValueError)` with a message like "Input must be a Pandas DataFrame".
3. **Test 2: HTML Content Generation**
   - **Goal:** Verify that the generated HTML contains the header, news items, and footer as specified.
   - **Assertion:** Check for presence of "MedNews", the date, and the specific fields of the mock data.
4. **Test 3: Successful Email Dispatch**
   - **Goal:** Verify that the email is correctly formatted as `MIMEMultipart` and sent.
   - **Assertion:** Check `mock_smtp.send_message` call count and arguments.
5. **Test 4: Error Handling**
   - **Goal:** Ensure the module handles SMTP exceptions gracefully.
   - **Assertion:** `pytest.raises(SMTPSenderError)` when `smtplib` raises an exception.

## Phase 2: Implementation (Green Phase)
**File:** `src/email_sender.py`

1. **Environment Config:**
   - Use `python-dotenv` to load: `SMTP_SERVER`, `SMTP_PORT`, `SENDER_EMAIL`, `SENDER_PASSWORD`, and `SUBSCRIBER_EMAIL`.
2. **HTML Template Design:**
   - **Header:** Background color `#2c3e50`, white text, "MedNews".
   - **Body:** News cards with white background, subtle border-radius, `title` as `<h3>`, `summary` as `<p>`, `link` as a beautiful CTA button.
   - **Footer:** Centered, small font, `#7f8c8d` color, showing `(c) 2026 MedNews`.
3. **Core Logic:**
   - Function: `send_news_email(news_df: pd.DataFrame)`.
   - Validate input: `if not isinstance(news_df, pd.DataFrame): raise ValueError(...)`.
   - Format current date: `datetime.now().strftime("%d/%m/%Y")`.
   - Loop over `news_df.iterrows()` to build news items.
   - Assemble `MIMEMultipart` with `MIMEText(html, 'html')`.
   - Connect to SMTP, `starttls`, `login`, and `send_message`.

## Phase 3: Refactor & Verification
1. Run `pytest tests/test_email_sender.py` to ensure all tests pass.
2. Review the code against KISS, DRY, and YAGNI principles.
3. Optimize the HTML/CSS for cross-client compatibility (Inline CSS).
4. Ensure proper logging and error messages.
