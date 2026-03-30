from dotenv import load_dotenv

try:
    from src.email_sender import send_news_email
    from src.filter_rss_data import filter_rss_data
    from src.rss_fetcher import fetch_rss_feed
    from src.translator import translate_feed
except ModuleNotFoundError:
    from email_sender import send_news_email
    from filter_rss_data import filter_rss_data
    from rss_fetcher import fetch_rss_feed
    from translator import translate_feed


def main() -> None:
    URL = "https://medicalxpress.com/rss-feed/"

    feed = fetch_rss_feed(URL)
    df = filter_rss_data(feed)
    df = translate_feed(df)

    send_news_email(df)


if __name__ == "__main__":
    load_dotenv()
    main()
