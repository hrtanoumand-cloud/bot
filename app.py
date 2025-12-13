from flask import Flask, request
import requests
import os
from urllib.parse import quote

app = Flask(__name__)

# مقادیر محیطی (Environment Variables)
BOT_TOKEN = os.getenv("BOT_TOKEN")
SUPABASE_URL = os.getenv("SUPABASE_URL")  # مثلا https://xyzcompany.supabase.co
SUPABASE_KEY = os.getenv("SUPABASE_KEY")  # Service Role Key یا Anon Key با دسترسی خواندن

@app.route("/", methods=["POST"])
def webhook():
    data = request.json

    if not data or "message" not in data:
        return "ok"

    chat_id = data["message"]["chat"]["id"]
    user_text = data["message"].get("text", "").strip()

    if not user_text:
        return "ok"

    # URL-encode کردن متن کاربر
    query = quote(user_text)
    url = f"{SUPABASE_URL}/rest/v1/responses?keyword=eq.{query}&select=answer"

    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Accept": "application/json"
    }

    answer = "❌ عبارتی با این متن پیدا نشد"

    try:
        r = requests.get(url, headers=headers, timeout=10)

        if r.status_code != 200:
            answer = f"❌ خطا در ارتباط با دیتابیس (کد {r.status_code})"
        else:
            result = r.json()
            if isinstance(result, list) and len(result) > 0:
                answer = result[0].get("answer", answer)

    except Exception as e:
        answer = f"❌ خطای غیرمنتظره در سرور: {str(e)}"

    # ارسال پاسخ به ربات بله
    try:
        requests.post(
            f"https://tapi.bale.ai/bot{BOT_TOKEN}/sendMessage",
            json={
                "chat_id": chat_id,
                "text": answer
            },
            timeout=10
        )
    except Exception as e:
        print(f"خطا در ارسال پیام به بله: {e}")

    return "ok"

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )
