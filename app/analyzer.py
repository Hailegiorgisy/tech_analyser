import os
from google import genai
from google.genai import types
from pydantic import BaseModel

class TechDigest(BaseModel):
    summary: str
    key_innovations: list[str]
    repo_recommendation: str

def generate_trend_digest(github_data: list, hn_data: list) -> TechDigest:
    """Passes scraped data to Gemini to produce a structured summary."""
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
    
    prompt = f"""
    You are an expert tech analyst. Analyze the following trending GitHub repositories and news stories:
    
    GitHub Repositories:
    {github_data}
    
    Hacker News Discussions:
    {hn_data}
    
    Provide a concise technical digest highlighting emerging patterns and standout projects.
    """
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=TechDigest,
            temperature=0.2,
        ),
    )
    
    return TechDigest.model_validate_json(response.text)