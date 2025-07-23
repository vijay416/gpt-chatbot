from flask import Flask, request, jsonify
from flask_cors import CORS  
import openai
import os

app = Flask(__name__)

# ✅ Allow CORS from all origins (or restrict to your domain)
CORS(app, origins=["https://optymise.in"])  # or CORS(app) to allow all

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/")
def home():
    return "GPT Chatbot API is running."

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message")

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": user_message}]
        )
        reply = response.choices[0].message["content"].strip()
        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
