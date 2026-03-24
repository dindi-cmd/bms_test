import requests
from bs4 import BeautifulSoup
import os

# ===== CONFIG =====
URL = "https://in.bookmyshow.com/movies/hyd/seat-layout/ET00492371/ALUC/193/20260326"

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# ===== CHECK FUNCTION =====
def check_availability():
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    res = requests.get(URL, headers=headers)
    html = res.text

    if "Sold Out" in html or "sold out" in html:
        return False
    return True


# ===== TELEGRAM ALERT =====
def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": msg
    })


# ===== MAIN =====
if __name__ == "__main__":
    available = check_availability()

    if available:
        send_telegram("🎟 Tickets might be AVAILABLE! Check now!")
    else:
        print("No tickets yet...")
