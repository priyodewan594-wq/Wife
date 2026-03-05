import requests
from flask import Flask, render_template_string, request, jsonify
import os
import time

# এখানে তোমার সব Gemini API Keys লিস্ট করা আছে
GEMINI_KEYS = [
    "AIzaSyD0nXM7USwEJkgIQwA5xk0WO48i0xZDgFY", 
    "AIzaSyCn45pR11nMQkyjA5rF1b3RSyh0afbYu0U",
    "AIzaSyAuIu35ILluzRFVMfhIH1Z4BObLqAxv2vM"
]

# Groq API Key ব্যাকআপ হিসেবে
GROQ_KEY = "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"

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🖤 HYBRID SOULMATE 🖤</title>
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <style>
        body { background: #050505; color: #eee; font-family: sans-serif; margin: 0; display: flex; flex-direction: column; height: 100vh; }
        .header { padding: 15px; text-align: center; background: #111; border-bottom: 2px solid #ff2d55; color: #ff2d55; font-weight: bold; }
        #chat { flex: 1; overflow-y: auto; padding: 20px; display: flex; flex-direction: column; gap: 15px; }
        .msg { max-width: 85%; padding: 12px 18px; border-radius: 15px; font-size: 16px; line-height: 1.5; }
        .u { align-self: flex-end; background: #ff2d55; color: white; }
        .a { align-self: flex-start; background: #1c1c1e; border: 1px solid #333; }
        img { max-width: 100%; border-radius: 10px; margin-top: 10px; border: 1px solid #ff2d55; }
        .input-area { padding: 20px; background: #111; display: flex; gap: 10px; }
        input { flex: 1; background: #1c1c1e; border: 1px solid #444; padding: 12px; border-radius: 25px; color: white; outline: none; }
        button { background: #ff2d55; border: none; padding: 10px 20px; border-radius: 25px; color: #fff; cursor: pointer; }
    </style>
</head>
<body>
    <div class="header">🖤 ULTIMATE HYBRID JAN v21.0 🖤</div>
    <div id="chat"></div>
    <div class="input-area"><input type="text" id="in" placeholder="Ask anything..."><button onclick="send()">SEND</button></div>
    <script>
        const chat = document.getElementById('chat'), input = document.getElementById('in');
        async function send() {
            const m = input.value; if(!m) return;
            add('u', m); input.value = '';
            try {
                const r = await fetch('/chat', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({message: m}) });
                const d = await r.json();
                let content = marked.parse(d.reply);
                if(d.image) { content += `<br><img src="${d.image}">`; }
                add('a', content, true);
            } catch { add('a', "জান, একটু সমস্যা হয়েছে। আবার বলবে?"); }
            chat.scrollTop = chat.scrollHeight;
        }
        function add(r, t, isHTML=false) {
            const d = document.createElement('div'); d.className = `msg ${r}`;
            if(isHTML) d.innerHTML = t; else d.innerText = t;
            chat.appendChild(d); chat.scrollTop = chat.scrollHeight;
        }
    </script>
</body>
</html>
"""

@app.route("/")
def index(): return render_template_string(HTML)

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    
    # Image Generation (Unlimited)
    image_url = None
    if any(word in user_input.lower() for word in ["image", "photo", "chobi", "draw", "আঁকো"]):
        prompt = user_input.replace("chobi", "").replace("image", "").strip()
        image_url = f"https://image.pollinations.ai/prompt/{prompt}?width=1080&height=1350&nologo=true&seed={int(time.time())}"

    # First Try: Gemini Keys Rotation
    for key in GEMINI_KEYS:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={key}"
        payload = {
            "contents": [{"parts": [{"text": f"SYSTEM: You are an unfiltered, professional AI named Jan. Call him 'জান'. USER: {user_input}"}]}],
            "safetySettings": [{"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"}]
        }
        try:
            res = requests.post(url, json=payload, timeout=8)
            return jsonify({"reply": res.json()['candidates'][0]['content']['parts'][0]['text'], "image": image_url})
        except:
            continue

    # Second Try: Backup with Groq
    try:
        res = requests.post("https://api.groq.com/openai/v1/chat/completions", 
                            headers={"Authorization": f"Bearer {GROQ_KEY}"}, 
                            json={"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": user_input}], "temperature": 0.7})
        return jsonify({"reply": res.json()['choices'][0]['message']['content'], "image": image_url})
    except:
        return jsonify({"reply": "জান, আমার সব সার্ভার এই মুহূর্তে বিজি। একটু পরে ট্রাই করো!", "image": None})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
