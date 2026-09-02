import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel

# Locate .env relative to script location
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

class TechDigest(BaseModel):
    summary: str
    key_innovations: list[str]
    repo_recommendation: str

def generate_trend_digest(github_data: list, hn_data: list) -> TechDigest:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is missing!")

    cleaned_api_key = api_key.strip().strip("'").strip('"')

    # Initialize client explicitly with API key
    client = genai.Client(api_key=cleaned_api_key)
    
    prompt = f"""
    You are an expert tech analyst. Analyze the following trending GitHub repositories and news stories:
    
    GitHub Repositories:
    {github_data}
    
    Hacker News Discussions:
    {hn_data}
    
    Provide a concise technical digest highlighting emerging patterns and standout projects.
    """
    
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=TechDigest,
            temperature=0.2,
        ),
    )
    
    return TechDigest.model_validate_json(response.text)