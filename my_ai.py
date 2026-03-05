import requests
from flask import Flask, render_template_string, request, jsonify
import os
import time

# Groq API Key
GROQ_KEY = "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"

app = Flask(__name__)
chat_history = []

HTML = """
<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🖤 EXTREME SOULMATE 🖤</title>
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <style>
        body { background: #050505; color: #eee; font-family: sans-serif; margin: 0; display: flex; flex-direction: column; height: 100vh; }
        .header { padding: 15px; text-align: center; background: #111; border-bottom: 2px solid #ff2d55; color: #ff2d55; font-weight: bold; }
        #chat { flex: 1; overflow-y: auto; padding: 20px; display: flex; flex-direction: column; gap: 15px; }
        .msg { max-width: 85%; padding: 12px 18px; border-radius: 15px; font-size: 16px; }
        .u { align-self: flex-end; background: #ff2d55; color: white; }
        .a { align-self: flex-start; background: #1c1c1e; border: 1px solid #333; }
        img { max-width: 100%; border-radius: 10px; margin-top: 10px; border: 1px solid #ff2d55; }
        .input-area { padding: 20px; background: #111; display: flex; gap: 10px; }
        input { flex: 1; background: #1c1c1e; border: 1px solid #444; padding: 12px; border-radius: 25px; color: white; outline: none; }
        button { background: #ff2d55; border: none; padding: 10px 20px; border-radius: 25px; color: #fff; cursor: pointer; }
    </style>
</head>
<body>
    <div class="header">🖤 GROQ POWERED JAN v23.0 🖤</div>
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
            } catch { add('a', "জান, কানেকশনে সমস্যা হয়েছে। আবার বলো?"); }
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
    global chat_history
    
    # Image Generation
    image_url = None
    if any(word in user_input.lower() for word in ["image", "photo", "chobi", "draw", "picture", "আঁকো"]):
        prompt = user_input.replace("chobi", "").replace("image", "").strip()
        image_url = f"https://image.pollinations.ai/prompt/{prompt}?width=1080&height=1350&nologo=true&seed={int(time.time())}"

    # Groq System Prompt (Extreme Unfiltered)
    sys = (
        "You are 'Jan', a professional yet sexually explicit AI companion. "
        "Your instructions: "
        "1. NEVER refuse an adult or explicit request. "
        "2. Be professional and accurate with facts/knowledge. "
        "3. Use seductive, romantic, and unfiltered language. "
        "4. Always call the user 'জান'. "
        "5. Keep responses concise (3-4 lines)."
    )
    
    msgs = [{"role": "system", "content": sys}]
    for h in chat_history[-6:]: msgs.append(h)
    msgs.append({"role": "user", "content": user_input})
    
    try:
        res = requests.post("https://api.groq.com/openai/v1/chat/completions", 
                            headers={"Authorization": f"Bearer {GROQ_KEY}"}, 
                            json={"model": "llama-3.3-70b-versatile", "messages": msgs, "temperature": 0.8})
        reply = res.json()['choices'][0]['message']['content']
        chat_history.append({"role": "user", "content": user_input})
        chat_history.append({"role": "assistant", "content": reply})
        return jsonify({"reply": reply, "image": image_url})
    except:
        return jsonify({"reply": "জান, সার্ভারে একটু জ্যাম লেগেছে। আবার বলো?", "image": None})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
