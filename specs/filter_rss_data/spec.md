# Spec: Filter RSS Data

## Description

This module is responsible for filtering data from RSS feeds. It must have three main responsabilities:

- Guarantee that some columns are present in the data (title, description, link, pubDate)
- Filter rows where title, description, link or pubDate are not null
- Select only the columns (title, description, link, pubDate)

## Acceptance criterias

- [v] When called, the module should receive a FeedParserDict object.
- [v] The module should return a pandas DataFrame with the filtered data.
- [v] If the data is not valid, the module should throw an exception.
- [v] The final result must have the following columns: **title**, **description**, **link**, **pubDate**

## Tests

- [v] Test the module receiving a FeedParserDict object.
- [v] Test if module return a pandas DataFrame with the filtered data.
- [v] Test if module throw an exception if feed data doesnt have the required columns.
- [v] Test if required columns doesnt contain null values.
