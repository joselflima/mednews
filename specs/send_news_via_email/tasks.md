# Tasks: Send News via Email

- [x] **Infrastructure Setup**
  - [x] Create `tests/test_email_sender.py`
  - [x] Add `pandas` and `python-dotenv` to `requirements.txt`
  - [x] Securely configure `.env` with SMTP credentials

- [x] **Phase 1: Red (Test Development)**
  - [x] **Test Setup:** Mock SMTP server class for testing.
  - [x] **Input Validation Test:** Assert failure when a non-DataFrame object is passed.
  - [x] **HTML Body Generation Test:** Verify that the HTML contains the expected news items.
  - [x] **Success Case Test:** Mock `smtplib.SMTP` and verify that `send_message` is called once.
  - [x] **Failure Case Test:** Verify that `SMTPException` triggers a custom exception.

- [x] **Phase 2: Green (Implementation)**
  - [x] Implement `src/email_sender.py`.
  - [x] Create a modern HTML/CSS template to represent medical news properly.
  - [x] Implement logic to convert DataFrame rows into HTML fragments.
  - [x] Implement SMTP connection and email dispatch logic with error handling.

- [x] **Phase 3: Refactor & Verification**
  - [x] Ensure proper type hinting and docstrings for all functions.
  - [x] Run `pytest tests/test_email_sender.py` to confirm all tests pass.
  - [x] Perform manual visual check of the generated HTML (optional, using a file output).
  - [x] Final check against KISS and DRY principles.
