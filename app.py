from flask import Flask, request
import requests

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_URL")

@app.route("/", methods=["POST"])
def webhook():
    data = request.json
    chat_id = data["message"]["chat"]["id"]
    user_text = data["message"].get("text", "").strip()

    url = f"{SUPABASE_URL}/rest/v1/responses?keyword=eq.{user_text}"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}"
    }

    r = requests.get(url, headers=headers)
    result = r.json()

    if result:
        answer = result[0]["answer"]
    else:
        answer = "❌ چیزی پیدا نشد"

    requests.post(
        f"https://tapi.bale.ai/bot{BOT_TOKEN}/sendMessage",
        json={"chat_id": chat_id, "text": answer}
    )

    return "ok"

app.run(port=5000)
