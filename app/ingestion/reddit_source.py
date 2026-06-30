import os
import praw
from dotenv import load_dotenv

load_dotenv()
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT")
)

def fetch_reddit(brand: str, limit: int = 20) -> list[dict]:
    results = []
    for submission in reddit.subreddit("all").search(brand, limit=limit, sort="new"):
        results.append({
            "text": f"{submission.title}. {submission.selftext[:500]}",
            "url": f"https://reddit.com{submission.permalink}",
            "published_at": str(submission.created_utc),
            "source": "reddit"
        })
    return results
