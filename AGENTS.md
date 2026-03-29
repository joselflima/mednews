# AGENTS

## Project directory

.
├── AGENTS.md               # Agents instructions
├── README.md               # Project documentation
├── arch.excalidraw         # Project architecture diagram
├── requirements.txt        # Python dependencies
├── specs                   # Project specifications
│   └── get_data_from_rss
│       ├── plan.md
│       ├── spec.md
│       └── tasks.md
├── src                     # Project source code
│   └── rss_fetcher.py
└── tests                   # Project tests
    └── test_rss_fetcher.py              

## Project technical specification

- Use TDD metodology to develop the project (red, green, refactor)
- Always develop tests before the implementation you are about to do
- Every time you write code, make sure that you're following KISS, DRY and YAGNI principles
- When you finish the implementation step, run tests and make sure that they are passing before moving to the next step
- You can just declare the entire task as completed when all tests are passing and code is clean and well-structured

## Tech stack

- Python
    - feedparser
    - pytest
    - smtplib
    - groq
    - python-dotenv

## Commands

- Testing:
```bash
python -m pytest tests/test_rss_fetcher.py
```
