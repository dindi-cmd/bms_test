import time
import os
import requests

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# ===== CONFIG =====
URL = "https://in.bookmyshow.com/movies/hyd/seat-layout/ET00492371/ALUC/193/20260326"

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

THRESHOLD = 30


# ===== TELEGRAM FUNCTION =====
def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    response = requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": msg
    })
    print("Telegram response:", response.text)


# ===== MAIN FUNCTION =====
def check_seats():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # IMPORTANT for GitHub
    options.binary_location = "/usr/bin/chromium-browser"

    service = Service("/usr/bin/chromedriver")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(URL)

    # wait for page load
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

    # scroll to ensure seats load
    time.sleep(5)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

    # ===== SEAT DETECTION =====
    seats = driver.find_elements(By.XPATH, "//a")

    available_count = 0

    for seat in seats:
        text = seat.text.strip()
        cls = (seat.get_attribute("class") or "").lower()

        # seat must have number
        if text.isdigit():

            # skip sold seats
            if "sold" in cls or "blocked" in cls:
                continue

            # skip selected seats (green filled)
            if "selected" in cls:
                continue

            # remaining = available
            available_count += 1

    print(f"Available seats: {available_count}")

    driver.quit()
    return available_count


# ===== RUN =====
if __name__ == "__main__":
    seats = check_seats()

    if seats > THRESHOLD:
        send_telegram(f"🎟 {seats} seats available! Book now!")
    else:
        print("Not enough seats yet...")
