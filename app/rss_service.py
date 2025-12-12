import feedparser
from .config import settings

def fetch_rss():
    try:
        feed = feedparser.parse(settings.RSS_URL)
        articles = []
        for item in feed.entries:
            articles.append({
                "title": item.title,
                "link": item.link,
                "summary": item.get("summary", "")
            })
        return articles
    except Exception as e:
        raise RuntimeError(f"RSS fetch error: {str(e)}")
