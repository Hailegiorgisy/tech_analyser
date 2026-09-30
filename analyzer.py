import os
import json
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import httpx
from google import genai
from google.genai import types

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

HN_TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
HN_ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

def fetch_top_tech_stories(limit: int = 5) -> list[dict]:
    stories = []
    try:
        with httpx.Client(timeout=10.0) as client:
            resp = client.get(HN_TOP_STORIES_URL)
            resp.raise_for_status()
            story_ids = resp.json()[:limit]

            for s_id in story_ids:
                item_resp = client.get(HN_ITEM_URL.format(s_id))
                if item_resp.status_code == 200:
                    data = item_resp.json()
                    stories.append({
                        "title": data.get("title", ""),
                        "url": data.get("url", f"https://news.ycombinator.com/item?id={s_id}"),
                        "score": data.get("score", 0)
                    })
    except Exception as e:
        logger.error(f"Error fetching stories: {e}")
    return stories

def generate_digest(stories: list[dict]) -> str:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        logger.warning("GEMINI_API_KEY missing. Generating plain text summary.")
        return "\n".join([f"- {s['title']} ({s['url']})" for s in stories])

    client = genai.Client(api_key=api_key)
    prompt = (
        "Summarize these trending technology developments into a concise daily briefing "
        "highlighting practical engineering impacts:\n\n" + json.dumps(stories, indent=2)
    )
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    return response.text

def main():
    stories = fetch_top_tech_stories(limit=6)
    if not stories:
        logger.warning("No tech stories retrieved; skipping digest.")
        return

    digest = generate_digest(stories)
    logger.info("Daily Tech Digest generated successfully.")
    print(digest)

if __name__ == "__main__":
    main()
