# Spec: Send news via email

## Objective

Users must receive a daily email with the latest news translated to Portuguese. All the data you need is passed by the translator module, which returns a DataFrame with the following columns:
**title**, **summary**, **link**, **published**. Your mission here is to implement a new feature to send an email to the user with the news. The email must have a modern, attractive and beautiful design.

## Design

- Header with the title "MedNews", subtitle "Seu resumo diário de notícias médicas" and the date
- Body with the news, each news with a title, summary, published date and link; the news must be separated by a horizontal line and a space between them.
- Footer with the text "MedNews" and the date. The footer must be centered and in a different color than the body. The footer must be in a smaller font size than the body. It must contains a "(c) 2026 MedNews. Todos os direitos reservados."

## Acceptance Criteria

- [] The module can be possible to receive a DataFrame with the news. If the input is not a DataFrame, the module must return an exception.
- [] The module must be possible to send an email to the user with the news. If the email is not sent, the module must return an exception.
- [] You must design the email body in HTML, but it must be responsive, modern, attractive and beautiful.
- [] If any problem with the SMTP happens, another exception must be raised.
- [] The email of the unique subscriber, by now, can be found in env as SUBSCRIBER_EMAIL.
