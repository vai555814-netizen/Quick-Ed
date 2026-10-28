import os
import requests
import google.generativeai as genai

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHANNEL = os.environ.get("TELEGRAM_CHANNEL_USERNAME")

genai.configure(api_key=GEMINI_API_KEY)
def generate_update():
    prompt = "You are an expert Indian education and exam news analyst. Generate a fresh, high-priority, factual educational update relevant to Indian students. Format in Inshorts style: under 60 words, catchy headline with emojis, key facts (Eligibility, Dates), no clutter."
    
    # Yeh code apne aap check kar lega ki teri key par kaun sa model chal raha hai
    model_name = 'gemini-3.8-flash'
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                model_name = m.name
                break
    except Exception as e:
        print("Model fetch error, using default:", e)
        
    print("Using Model:", model_name)
    model = genai.GenerativeModel(model_name)
    response = model.generate_content(prompt)
    return response.text
def send_to_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHANNEL, "text": text, "parse_mode": "Markdown"}
    response = requests.post(url, json=payload)
    print("Telegram Response:", response.text)

if __name__ == "__main__":
    update_text = generate_update()
    if update_text:
        send_to_telegram(update_text)
