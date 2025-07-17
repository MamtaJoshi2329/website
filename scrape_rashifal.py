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

CATEGORIES = ["daily", "weekly", "monthly", "yearly", "muhurat", "nakshatra"]

BASE_URLS = {
    "daily": "https://www.drikpanchang.com/astrology/rashifal/{1}-rashifal.html",
    "weekly": "https://www.drikpanchang.com/astrology/rashifal/weekly/{}-weekly-rashifal.html",
    "monthly": "https://www.drikpanchang.com/astrology/rashifal/monthly/{}-monthly-rashifal.html",
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
    # Fetch the main DenikPanchang rashifal page
    url = "https://www.drikpanchang.com/astrology/prediction/vedic-astrology-rashiphal.html"
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    # For each sign, extract English and Hindi predictions
    for slug, name in SIGNS:
        sign_data = {}
        # Find the English prediction
        en_block = soup.find("div", string=lambda s: s and name in s)
        en_text = ""
        hi_text = ""
        if en_block:
            # The prediction is usually in the next sibling <div>
            en_pred = en_block.find_next("div")
            if en_pred:
                en_text = en_pred.text.strip()
            # The Hindi prediction is usually after the English one
            hi_block = en_pred.find_next("div") if en_pred else None
            if hi_block:
                hi_text = hi_block.text.strip()
        sign_data["daily"] = {"en": en_text, "hi": hi_text}
        # Leave other categories empty for now
        for cat in ["weekly", "monthly", "yearly", "muhurat", "nakshatra"]:
            sign_data[cat] = {"en": "", "hi": ""}
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