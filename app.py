import json
import datetime
from flask import Flask, render_template, url_for, request, redirect

app = Flask(__name__)

RASHIS = [
    {"en": "Aries", "hi": "मेष", "icon": "\u2648", "img": "aries.png"},
    {"en": "Taurus", "hi": "वृषभ", "icon": "\u2649", "img": "taurus.png"},
    {"en": "Gemini", "hi": "मिथुन", "icon": "\u264A", "img": "gemini.png"},
    {"en": "Cancer", "hi": "कर्क", "icon": "\u264B", "img": "cancer.png"},
    {"en": "Leo", "hi": "सिंह", "icon": "\u264C", "img": "leo.png"},
    {"en": "Virgo", "hi": "कन्या", "icon": "\u264D", "img": "virgo.png"},
    {"en": "Libra", "hi": "तुला", "icon": "\u264E", "img": "libra.png"},
    {"en": "Scorpio", "hi": "वृश्चिक", "icon": "\u264F", "img": "scorpio.png"},
    {"en": "Sagittarius", "hi": "धनु", "icon": "\u2650", "img": "sagittarius.png"},
    {"en": "Capricorn", "hi": "मकर", "icon": "\u2651", "img": "capricorn.png"},
    {"en": "Aquarius", "hi": "कुंभ", "icon": "\u2652", "img": "aquarius.png"},
    {"en": "Pisces", "hi": "मीन", "icon": "\u2653", "img": "pisces.png"}
]

CATEGORIES = ["daily", "weekly", "monthly", "yearly", "muhurat", "nakshatra"]
LANGUAGES = ["en", "hi"]
LANG_LABELS = {"en": "English", "hi": "हिन्दी"}

@app.route('/')
def home():
    return render_template('rashifal_home.html', rashis=RASHIS)

@app.route('/rashifal/<rashi>/', defaults={'category': 'daily', 'lang': 'en'})
@app.route('/rashifal/<rashi>/<category>/', defaults={'lang': 'en'})
@app.route('/rashifal/<rashi>/<category>/<lang>')
def rashifal(rashi, category, lang):
    rashi_obj = next((r for r in RASHIS if r["en"].lower() == rashi.lower()), None)
    if not rashi_obj or category not in CATEGORIES or lang not in LANGUAGES:
        return render_template('404.html'), 404
    today = datetime.date.today().isoformat()
    try:
        with open('rashifal_data.json', encoding='utf-8') as f:
            data = json.load(f)
        day_data = data.get(today, {})
        sign_data = day_data.get(rashi_obj["en"], {})
        rashifal_text = sign_data.get(category, {}).get(lang, "No Rashifal available.")
    except Exception:
        rashifal_text = "No Rashifal available."
    # For tab navigation
    all_texts = {cat: {l: sign_data.get(cat, {}).get(l, "") for l in LANGUAGES} for cat in CATEGORIES}
    return render_template(
        'rashifal_detail.html',
        rashi=rashi_obj["en"],
        rashi_hi=rashi_obj["hi"],
        icon=rashi_obj["icon"],
        img=rashi_obj["img"],
        now=datetime.date.today(),
        category=category,
        lang=lang,
        categories=CATEGORIES,
        languages=LANGUAGES,
        lang_labels=LANG_LABELS,
        rashifal_text=rashifal_text,
        all_texts=all_texts
    )

if __name__ == '__main__':
    app.run(debug=True) 