import os
import httpx
from dotenv import load_dotenv

load_dotenv()

async def send_telegram_alert(message: str, show_button: bool = False):
    """
    Dispatches notifications to the designated Telegram communication channel.
    Injects inline dashboard routing triggers if show_button evaluation resolves to True.
    """
    token = os.getenv("TELEGRAM_TOKEN", "").strip()
    chat_id = os.getenv("TELEGRAM_CHAT_ID", "").strip()
    
    if not token or not chat_id:
        print("Log: Telegram credential tokens are not defined in the workspace context.")
        return

    url = f"https://api.telegram.org/{token}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }

    if show_button:
        callback_url = "http://127.0.0" 
        payload["reply_markup"] = {
            "inline_keyboard": [
                [
                    {
                        "text": "Log Irrigation Cycle via Swagger",
                        "url": callback_url
                    }
                ]
            ]
        }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=payload, timeout=10.0)
            if response.status_code == 200:
                print("Log: Telegram notification payload dispatched successfully.")
            else:
                print(f"Error: Telegram API returned structural failure code {response.status_code}: {response.text}")
        except Exception as e:
            print(f"Network error processing Telegram message payload connection: {e}")
