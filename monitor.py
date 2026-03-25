import time
import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# ✅ VERY IMPORTANT (fix chrome path)
options.binary_location = "/usr/bin/chromium-browser"

# ✅ VERY IMPORTANT (fix driver path)
service = Service("/usr/bin/chromedriver")

driver = webdriver.Chrome(service=service, options=options)

# ===== CONFIG =====
URL = "https://in.bookmyshow.com/movies/hyd/seat-layout/ET00492371/ALUC/193/20260326"

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

THRESHOLD = 30


# ===== TELEGRAM FUNCTION =====
def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": msg
    })


# ===== MAIN FUNCTION =====
def check_seats():
    options = Options()
    options.add_argument("--headless")  # run without opening browser
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(URL)

    time.sleep(5)  # wait for seats to load

    # find available seats
    seats = driver.find_elements(By.CSS_SELECTOR, "[class*='available']")
    available_count = len(seats)

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
