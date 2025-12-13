from flask import Flask, request
import requests

app = Flask(__name__)

BOT_TOKEN = "701157315:XDmG4q7-piljOKPwehXPpFEEzogyCkcN8JA"
SUPABASE_URL = "https://znasqapborqzekhaahmv.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpuYXNxYXBib3JxemVraGFhaG12Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjU2NDI1OTgsImV4cCI6MjA4MTIxODU5OH0.-Kb8Taz58YjjzZBVqTr_TmmzdsAYqEI2miQYmzoEXHM"

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