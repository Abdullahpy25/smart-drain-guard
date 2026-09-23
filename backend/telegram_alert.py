import os
import requests
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


def send_telegram_alert(drain_id, blockage, risk_score):
    if not BOT_TOKEN or not CHAT_ID:
        raise ValueError("Telegram credentials are missing.")

    message = (
        "🚨 Smart Drain Guard Alert\n\n"
        f"Drain: {drain_id}\n"
        f"Blockage: {blockage}%\n"
        f"Risk Score: {risk_score}\n"
        "Status: RED"
    )

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    response = requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "text": message
        },
        timeout=10
    )

    response.raise_for_status()

    return response.json()


if __name__ == "__main__":
    result = send_telegram_alert(
        "drain1",
        90,
        72.3
    )

    print("Telegram alert sent successfully.")