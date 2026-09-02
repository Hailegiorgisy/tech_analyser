import os
import httpx
from app.analyzer import TechDigest

async def send_telegram_notification(digest: TechDigest) -> None:
    """Formats and sends the TechDigest to a Telegram chat or channel."""
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")

    if not bot_token or not chat_id:
        print("⚠️ TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not set. Skipping Telegram dispatch.")
        return

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    # Format text using HTML tags supported by Telegram API
    innovations_list = "\n".join([f"• {item}" for item in digest.key_innovations])

    message_text = (
        f"<b>🚀 Daily Tech & Repo Trend Digest</b>\n\n"
        f"<b>📌 Summary:</b>\n{digest.summary}\n\n"
        f"<b>💡 Key Innovations:</b>\n{innovations_list}\n\n"
        f"<b>⭐ Featured Project:</b>\n{digest.repo_recommendation}"
    )

    payload = {
        "chat_id": chat_id,
        "text": message_text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload)
        if response.status_code == 200:
            print("✅ Successfully dispatched digest to Telegram!")
        else:
            print(f"❌ Failed to send to Telegram: {response.status_code} - {response.text}")