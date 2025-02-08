
from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# LINE Bot Credentials (Set these in Render Environment Variables)
LINE_ACCESS_TOKEN = os.getenv("LINE_ACCESS_TOKEN")

# Rule-based chatbot knowledge base
carbon_faqs = {
    "what is carbon neutrality": "Carbon neutrality means balancing the amount of greenhouse gases emitted with an equivalent amount removed from the atmosphere.",
    "how to achieve carbon neutrality": "Carbon neutrality can be achieved by reducing emissions, using renewable energy, and investing in carbon offset programs.",
    "examples of carbon neutral companies": "Companies like Google, Microsoft, and Apple have committed to carbon neutrality by reducing emissions and investing in carbon offset projects.",
    "what are carbon offsets": "Carbon offsets are projects that reduce CO2 emissions, such as reforestation, renewable energy, and carbon capture technologies.",
}

@app.route("/", methods=["GET"])
def home():
    return "LINE Chatbot is running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    print("📩 FULL RECEIVED REQUEST:", data)  # Debugging log

    if "events" in data and len(data["events"]) > 0:
        event = data["events"][0]
        reply_token = event.get("replyToken", None)
        user_message = event.get("message", {}).get("text", "").lower()

        # Handling complex interactions with multiple intents
        reply_text = None
        if "carbon neutrality" in user_message or "carbon footprint" in user_message:
            reply_text = carbon_faqs.get("what is carbon neutrality")
        elif "how to" in user_message and "achieve" in user_message:
            reply_text = carbon_faqs.get("how to achieve carbon neutrality")
        elif "examples" in user_message or "companies" in user_message:
            reply_text = carbon_faqs.get("examples of carbon neutral companies")
        elif "offset" in user_message:
            reply_text = carbon_faqs.get("what are carbon offsets")
        else:
            reply_text = "I can help with carbon neutrality! Ask me anything."

        if reply_token and reply_text:
            reply_message(reply_token, reply_text)

    return jsonify({"status": "ok"}), 200

def reply_message(reply_token, text):
    url = "https://api.line.me/v2/bot/message/reply"
    headers = {
        "Authorization": f"Bearer {LINE_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "replyToken": reply_token,
        "messages": [{"type": "text", "text": text}]
    }
    
    response = requests.post(url, headers=headers, json=data)
    print("📤 Sending reply:", response.status_code, response.text)  # Debugging log

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
