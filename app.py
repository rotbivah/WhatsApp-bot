from flask import Flask, request
import requests
import json

app = Flask(__name__)

# Replace with your WhatsApp Cloud API credentials
ACCESS_TOKEN = "YOUR_WHATSAPP_CLOUD_API_ACCESS_TOKEN"
VERIFY_TOKEN = "YOUR_VERIFY_TOKEN"

# WhatsApp API URL
WHATSAPP_API_URL = "https://graph.facebook.com/v17.0/YOUR_PHONE_NUMBER_ID/messages"

@app.route("/", methods=["GET"])
def verify():
    """Verifies the webhook with the token."""
    token_sent = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if token_sent == VERIFY_TOKEN:
        return challenge
    return "Verification failed", 403

@app.route("/", methods=["POST"])
def webhook():
    """Handles incoming messages from WhatsApp."""
    data = request.get_json()

    if "entry" in data:
        for entry in data["entry"]:
            for change in entry["changes"]:
                if "messages" in change["value"]:
                    for message in change["value"]["messages"]:
                        phone_number = message["from"]
                        message_text = message["text"]["body"]

                        # Reply to the sender
                        send_message(phone_number, f"Received: {message_text}")

    return "OK", 200

def send_message(phone, text):
    """Sends a message via WhatsApp Cloud API."""
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": phone,
        "text": {"body": text}
    }

    response = requests.post(WHATSAPP_API_URL, headers=headers, json=data)
    return response.json()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
