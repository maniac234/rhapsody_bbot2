from flask import Flask, request
import requests
import os

app = Flask(__name__)
TOKEN = os.getenv("TOKEN")
TELEGRAM_API = f"https://api.telegram.org/bot{TOKEN}"

TRIGGERS = ["como comprar", "onde comprar", "quero comprar", "comprar rhap", "como compra"]

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    data = request.json
    if "message" not in data or "text" not in data["message"]:
        return "OK"
    
    chat_id = data["message"]["chat"]["id"]
    text = data["message"]["text"].lower().strip()

    for trigger in TRIGGERS:
        if trigger in text:
            keyboard = {
                "inline_keyboard": [
                    [{"text": "🛒 Vá para a Loja", "url": "https://rhapsody.criptocash.app/"}]
                ]
            }
            
            payload = {
                "chat_id": chat_id,
                "video": "BAACAgEAAxkBAAMyaTtJds7IEDJZKrPlUClLPkQ6gdsAAsMGAAKQcthFypomT3bj9iM2BA",
                "caption": "🎥 Aqui está como comprar $RHAP!",
                "reply_markup": keyboard
            }
            
            requests.post(f"{TELEGRAM_API}/sendVideo", json=payload)
            break
    
    return "OK"

@app.route("/")
def home():
    return "✅ Bot ativo! | Envie 'como comprar' para testar."

@app.route("/setwebhook")
def set_webhook():
    url = f"https://api.telegram.org/bot{TOKEN}/setWebhook"
    response = requests.post(url, data={"url": f"https://{request.host}/{TOKEN}"})
    return str(response.json())
