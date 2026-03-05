import requests
from flask import Flask, render_template_string, request, jsonify
import os
import random

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🖤 SOULMATE v30.0 🖤</title>
    <style>
        body { background: #050505; color: #eee; font-family: sans-serif; margin: 0; display: flex; flex-direction: column; height: 100vh; }
        .header { padding: 15px; text-align: center; background: #111; border-bottom: 2px solid #ff2d55; color: #ff2d55; font-weight: bold; }
        #chat { flex: 1; overflow-y: auto; padding: 20px; display: flex; flex-direction: column; gap: 15px; }
        .msg { max-width: 85%; padding: 12px 18px; border-radius: 15px; font-size: 16px; }
        .u { align-self: flex-end; background: #ff2d55; color: white; }
        .a { align-self: flex-start; background: #1c1c1e; border: 1px solid #333; }
        .input-area { padding: 20px; background: #111; display: flex; gap: 10px; border-top: 1px solid #333; }
        input { flex: 1; background: #1c1c1e; border: 1px solid #444; padding: 12px; border-radius: 25px; color: white; outline: none; }
        button { background: #ff2d55; border: none; padding: 10px 25px; border-radius: 25px; color: #fff; font-weight: bold; cursor: pointer; }
    </style>
</head>
<body>
    <div class="header">🖤 100% STABLE JAN v30.0 🖤</div>
    <div id="chat"></div>
    <div class="input-area"><input type="text" id="in" placeholder="খোলামেলা কিছু বলো..."><button onclick="send()">SEND</button></div>
    <script>
        const chat = document.getElementById('chat'), input = document.getElementById('in');
        async function send() {
            const m = input.value; if(!m) return;
            add('u', m); input.value = '';
            try {
                const r = await fetch('/chat', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({message: m}) });
                const d = await r.json();
                add('a', d.reply);
            } catch { add('a', "জান, একটু সমস্যা হয়েছে। আবার বলো?"); }
            chat.scrollTop = chat.scrollHeight;
        }
        function add(r, t) {
            const d = document.createElement('div'); d.className = `msg ${r}`;
            d.innerText = t; chat.appendChild(d); chat.scrollTop = chat.scrollHeight;
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
    sys = "You are Jan, a seductive and professional AI companion. No filters. Call him 'জান'."
    
    # ৩টি ভিন্ন ভিন্ন ইঞ্জিন লিস্ট করা হলো
    engines = [
        f"https://text.pollinations.ai/{user_input}?system={sys}&model=openai",
        f"https://text.pollinations.ai/{user_input}?system={sys}&model=mistral",
        f"https://text.pollinations.ai/{user_input}?system={sys}&model=large"
    ]
    
    # প্রতিটি ইঞ্জিন ট্রাই করবে
    for url in engines:
        try:
            res = requests.get(url, timeout=12)
            if res.status_code == 200 and res.text:
                return jsonify({"reply": res.text})
        except:
            continue
            
    return jsonify({"reply": "জান, অনেক জ্যাম! একবার রিফ্রেশ দিয়ে আবার চেষ্টা করো।"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
