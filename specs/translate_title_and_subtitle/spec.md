# Spec: Translate Title and Subtitle

## Objetive

Translate the title and subtitle of the RSS feed entries to Portuguese. To implement it, use the Groq API with the model Gemma 7B. The API key is stored in the environment variable GROQ_API_KEY.

## Acceptance Criterias

- [] When called, the module should receive a pandas DataFrame with the following columns: **title**, **summary**, **link**, **published**
- [] Verify if title and summary are present on the DataFrame and are not null.
- [] For each row, the module should select the **title** and **summary** columns and create a JSON format for the LLM with the following structure: {'title': 'title', 'description': 'description'}
- [] The module should translate the **title** and **summary** columns to Portuguese using the Groq API with the model Gemma 7B.
- [] It must verify if the Groq API result can be parsed as JSON.
- [] It must verify if the Groq API result contains the keys **title** and **description**.
- [] The module should return a pandas DataFrame with the translated columns.

## Tests

- [] Test the module receiving a pandas DataFrame with the following columns: **title**, **summary**, **link**, **published**
- [] Test if title and summary are present on the DataFrame and are not null.
- [] Test if module when passing a DataFrame without title or summary and check if it throws an exception.
- [] Test if LLM response can be parsed as JSON.
- [] Test if LLM response contains the keys **title** and **description**.
- [] Test if, when LLM response doesnt have the keys **title** and **description** or can't be parsed as JSON, the module throws an exception.
- [] Test if module return a pandas DataFrame with one row and the translated columns.

## Code example

```python
import groq
from groq import Groq

client = Groq()

try:
    client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a translator from English to Portuguese. Your answer must be a JSON object with the following structure: {'title': 'translated title', 'description': 'translated description'}",
            },
            {
                "role": "user",
                "content": f"{{'title': '{title}', 'description': '{description}'}}",
            }
        ],
        model="google/gemma-7b",
        temperature=0.1
    )
except groq.APIConnectionError as e:
    print("The server could not be reached")
    print(e.__cause__)  # an underlying Exception, likely raised within httpx.
except groq.RateLimitError as e:
    print("A 429 status code was received; we should back off a bit.")
except groq.APIStatusError as e:
    print("Another non-200-range status code was received")
    print(e.status_code)
    print(e.response)
```
