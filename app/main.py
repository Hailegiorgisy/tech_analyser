import asyncio
import json
import os
from dotenv import load_dotenv
from app.scraper import fetch_trending_github_repos, fetch_top_hn_stories
from app.analyzer import generate_trend_digest

load_dotenv()

async def main():
    print("🚀 Fetching raw data...")
    github_repos = await fetch_trending_github_repos(limit=5)
    hn_stories = await fetch_top_hn_stories(limit=5)
    
    print("🤖 Processing with LLM...")
    digest = generate_trend_digest(github_repos, hn_stories)
    
    print("\n--- DAILY TECH DIGEST ---")
    print(json.dumps(digest.model_dump(), indent=2))
    
    # Save output as a JSON artifact for downstream CI/CD tasks
    os.makedirs("output", exist_ok=True)
    with open("output/digest.json", "w") as f:
        json.dump(digest.model_dump(), f, indent=2)
        
    print("\n✅ Digest successfully created in output/digest.json!")

if __name__ == "__main__":
    asyncio.run(main())