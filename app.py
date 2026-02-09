import os, requests
from flask import Flask, request

app = Flask(__name__)

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "verify_token_123")
WA_TOKEN = os.getenv("WA_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")

def send_whatsapp(to, text):
    url = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages"
    headers = {"Authorization": f"Bearer {WA_TOKEN}"}
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": text}
    }
    requests.post(url, headers=headers, json=payload, timeout=20)

@app.get("/webhook")
def verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    return "Forbidden", 403

@app.post("/webhook")
def inbound():
    data = request.get_json() or {}
    try:
        msg = data["entry"][0]["changes"][0]["value"]["messages"][0]
        from_no = msg["from"]
        text = msg.get("text", {}).get("body", "")
        send_whatsapp(from_no, f"🤖 BHOLA: {text}")
    except:
        pass
    return "ok", 200

@app.get("/")
def home():
    return "BHOLA webhook running"

if __name__ == "__main__":
    app.run()
