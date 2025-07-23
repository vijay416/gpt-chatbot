from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

# Load your OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI()

# Create Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all domains

@app.route("/", methods=["GET"])
def home():
    return "✅ GPT Chatbot API is running."

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "").strip()

    if not message:
        return jsonify({"error": "No message provided"}), 400

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # or "gpt-4" if you have access
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": message}
            ],
            temperature=0.7,
            max_tokens=300
        )

        reply = response.choices[0].message.content.strip()
        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Optional: for Render health check
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

# Run the app locally (not used on Render/Railway)
if __name__ == "__main__":
    app.run(debug=True)
