from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session
from .database import SessionLocal
from .rss_service import fetch_rss
from .classify_service import classify_article
from .email_service import send_email
from .models import Article
from .utils import retry

import asyncio

# Job function
async def process_rss_job():
    print("=" * 80)
    print("🔄 RSS Job Started - Processing RSS feeds...")
    print("=" * 80)

    db: Session = SessionLocal()
    try:
        print("📡 Fetching RSS feeds...")
        articles = retry(fetch_rss)
        print(f"✅ Fetched {len(articles)} articles from RSS feed")

        new_items = []

        for item in articles:
            print(f"\n📰 Processing article: {item['title'][:60]}...")
            exists = db.query(Article).filter(Article.link == item["link"]).first()
            if exists:
                print(f"⏭️  Skipped (already exists in database)")
                continue  # Skip duplicates

            print(f"🤖 Classifying article...")
            category = await classify_article(item["title"], item["summary"])
            print(f"✅ Category: {category}")

            article = Article(
                title=item["title"],
                link=item["link"],
                summary=item["summary"],
                category=category
            )
            db.add(article)
            db.commit()
            print(f"💾 Saved to database")

            new_items.append(f"{item['title']} ({category})")

        if new_items:
            print(f"\n📧 Sending email with {len(new_items)} new articles...")
            send_email("RSS Summary Update", "\n".join(new_items))
            print(f"✅ Email sent successfully")
        else:
            print(f"\n📭 No new articles to send")

        print("\n" + "=" * 80)
        print(f"✅ RSS Job Completed - Processed {len(new_items)} new articles")
        print("=" * 80)

    finally:
        db.close()

def start_scheduler():
    print("\n🚀 Starting RSS Scheduler - Running every 5 minutes")
    scheduler = BackgroundScheduler()
    scheduler.add_job(lambda: asyncio.run(process_rss_job()), "interval", hours=4)
    scheduler.start()
    print("✅ Scheduler started successfully\n")

def stop_scheduler(scheduler: BackgroundScheduler):
    print("\n🛑 Stopping RSS Scheduler")
    scheduler.shutdown()
    print("✅ Scheduler stopped successfully\n")