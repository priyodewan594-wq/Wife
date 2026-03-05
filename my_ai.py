from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# এখানে আপনি চাইলে Groq বা Hugging Face এর আনফিল্টারড মডেল লিঙ্ক করতে পারেন
API_URL = "YOUR_MODEL_ENDPOINT" 
HEADERS = {"Authorization": "Bearer YOUR_TOKEN"}

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message")
    # এখানে আনফিল্টারড প্রম্পট ইঞ্জিনিয়ারিং যোগ করা যায়
    payload = {"inputs": f"[INST] {user_input} [/INST]"} 
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
