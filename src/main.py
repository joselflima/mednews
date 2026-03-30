from dotenv import load_dotenv
import json

from rss_fetcher import fetch_rss_feed
from filter_rss_data import filter_rss_data
from translator import translate_feed


def main():
    URL = "https://medicalxpress.com/rss-feed/"

    feed = fetch_rss_feed(URL)
    df = filter_rss_data(feed)
    df = translate_feed(df)
    
    print(df.head(5))


if __name__ == "__main__":
    load_dotenv()
    main()
