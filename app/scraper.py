import httpx
from typing import List, Dict, Any

async def fetch_trending_github_repos(limit: int = 5) -> List[Dict[str, Any]]:
    """Fetches top trending repositories created/updated recently."""
    url = "https://api.github.com/search/repositories?q=created:>2026-01-01&sort=stars&order=desc"
    headers = {"User-Agent": "TechTrendBot/1.0"}
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        repos = []
        for item in data.get("items", [])[:limit]:
            repos.append({
                "name": item["full_name"],
                "url": item["html_url"],
                "stars": item["stargazers_count"],
                "description": item["description"] or "No description provided."
            })
        return repos

async def fetch_top_hn_stories(limit: int = 5) -> List[Dict[str, Any]]:
    """Fetches top tech stories from Hacker News."""
    top_ids_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(top_ids_url)
        response.raise_for_status()
        story_ids = response.json()[:limit]
        
        stories = []
        for story_id in story_ids:
            item_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
            res = await client.get(item_url)
            if res.status_code == 200:
                data = res.json()
                stories.append({
                    "title": data.get("title"),
                    "url": data.get("url", f"https://news.ycombinator.com/item?id={story_id}"),
                    "score": data.get("score")
                })
        return stories