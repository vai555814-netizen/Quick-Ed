import os
import requests
import random
import google.generativeai as genai
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHANNEL = os.environ.get("TELEGRAM_CHANNEL_USERNAME")
genai.configure(api_key=GEMINI_API_KEY)
categories = [
    "All School & Board Exams (UP Board, CBSE, ICSE, State Boards) Timetables, Practical Dates, Result Notices, Syllabus & Official Alerts (#BoardUpdate)",
    "All National & State Entrance Exams (JEE, NEET, CUET, GATE, CAT, UPSC Prelims, NDA, CDS, CLAT, State PSCs) Admit Cards, Dates & Alerts (#Entrance)",
    "All Higher Education & Graduation University Updates (BA, BSc, BCom, MA, MSc, Professional Degrees) Exam Forms, Routine, Syllabus & Results (#Graduation)",
    "All Government Jobs, Railway RRB, SSC, Banking, UPSC, Teacher Recruitment, Police, Defence & Public Sector Vacancies & Notifications (#GovtJobs)"
]
def generate_update():
    chosen_cat = random.choice(categories)
    prompt = f"Focus Area: {chosen_cat}. STRICT RULE: Generate ONLY current, latest, and freshly released official updates. If no fresh news exists, reply with ONLY: NO_UPDATE."
    prompt += " Format in Inshorts style (under 60 words): Catchy Emoji Headline, bold key facts, proper hashtag, and official link."
    model = genai.GenerativeModel('gemini-3.8-flash')
    response = model.generate_content(prompt)
    text = response.text.strip()
    if "NO_UPDATE" in text or len(text) < 10: return None
       return text
def send_to_telegram(text):
    if not text: return
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHANNEL, "text": text, "parse_mode": "Markdown"}
    requests.post(url, json=payload)
    if __name__ == "__main__":
      update_text = generate_update()
    if update_text: send_to_telegram(update_text)
