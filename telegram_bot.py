import os
import httpx
from dotenv import load_dotenv

load_dotenv()

async def send_telegram_alert(message: str, show_button: bool = False):
    """
    Dispatches notifications to Telegram with static base path declarations.
    Bypasses string formatting bugs by explicitly declaring the server endpoints.
    """
    token = os.getenv("TELEGRAM_TOKEN", "").replace("\r", "").replace("\n", "").strip()
    chat_id = os.getenv("TELEGRAM_CHAT_ID", "").replace("\r", "").replace("\n", "").strip()
    
    if token.lower().startswith("bot"):
        token = token[3:]

    if not token or not chat_id:
        print("Log: Telegram credential tokens are not defined in the workspace context.")
        return

    # EXPLICIT STRUCTURAL BASE: Hardcoded absolute server path configuration
    # This prevents Docker from dropping the subdomains or path slashes
    url = "https://api.telegram.org/bot" + token + "/sendMessage"
    

    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }

    # Injecting the structural inline button matrix safely
    if show_button:
        # Telegram requires a valid public HTTPS URL for inline buttons.
        # Replace this placeholder link with your real public repository or live site URL later.
        production_dashboard_url = "https://github.com" 
        
        payload["reply_markup"] = {
            "inline_keyboard": [
                [
                    {
                        "text": "💧 Mark as Watered",
                        "url": production_dashboard_url
                    }
                ]
            ]
        }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=payload, timeout=10.0)
            if response.status_code == 200:
                print("Log: Optimized notification payload dispatched successfully.")
            else:
                print(f"Error: Telegram API failure code {response.status_code}: {response.text}")
        except Exception as e:
            print(f"Network error processing Telegram connection: {e}")