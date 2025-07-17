import requests
from bs4 import BeautifulSoup
import json
from datetime import date

SIGNS = [
    ("aries", "Aries"),
    ("taurus", "Taurus"),
    ("gemini", "Gemini"),
    ("cancer", "Cancer"),
    ("leo", "Leo"),
    ("virgo", "Virgo"),
    ("libra", "Libra"),
    ("scorpio", "Scorpio"),
    ("sagittarius", "Sagittarius"),
    ("capricorn", "Capricorn"),
    ("aquarius", "Aquarius"),
    ("pisces", "Pisces"),
]

CATEGORIES = ["daily", "weekly", "yearly", "muhurat", "nakshatra"]

BASE_URLS = {
    "daily": "https://www.drikpanchang.com/astrology/rashifal/{}-rashifal.html",
    "weekly": "https://www.drikpanchang.com/astrology/rashifal/weekly/{}-weekly-rashifal.html",
    "yearly": "https://www.drikpanchang.com/astrology/rashifal/yearly/{}-yearly-rashifal.html",
    "muhurat": "https://www.drikpanchang.com/astrology/muhurat/{}-muhurat.html",
    "nakshatra": "https://www.drikpanchang.com/astrology/nakshatra/{}-nakshatra.html",
}

SELECTORS = {
    # These are placeholder selectors. You must inspect the HTML and update them.
    "en": ".dpRashiContent .dpRashiContentEng",
    "hi": ".dpRashiContent .dpRashiContentHin"
}

def scrape_rashifal():
    today = date.today().isoformat()
    all_data = {}
    for slug, name in SIGNS:
        sign_data = {}
        for cat in CATEGORIES:
            url = BASE_URLS[cat].format(slug)
            resp = requests.get(url)
            soup = BeautifulSoup(resp.text, "html.parser")
            en = soup.select_one(SELECTORS["en"])
            hi = soup.select_one(SELECTORS["hi"])
            sign_data[cat] = {
                "en": en.text.strip() if en else "",
                "hi": hi.text.strip() if hi else ""
            }
        all_data[name] = sign_data
    # Save to JSON
    try:
        with open("rashifal_data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}
    data[today] = all_data
    with open("rashifal_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    scrape_rashifal() 