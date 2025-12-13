from flask import Flask, request
import requests
import os

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


@app.route("/", methods=["POST"])
def webhook():
    data = request.json

    if not data or "message" not in data:
        return "ok"

    chat_id = data["message"]["chat"]["id"]
    user_text = data["message"].get("text", "").strip()

    if not user_text:
        return "ok"

    url = f"{SUPABASE_URL}/rest/v1/responses?keyword=eq.{user_text}"

    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Accept": "application/json"
    }

    answer = "❌ عبارتی با این متن پیدا نشد"

    try:
        r = requests.get(url, headers=headers, timeout=10)

        # اگر Supabase خطا داد
        if r.status_code != 200:
            answer = "❌ خطا در ارتباط با دیتابیس"
        else:
            result = r.json()

            # اگر خروجی لیست بود و حداقل یک رکورد داشت
            if isinstance(result, list) and len(result) > 0:
                if isinstance(result[0], dict) and "answer" in result[0]:
                    answer = result[0]["answer"]

    except Exception as e:
        answer = "❌ خطای غیرمنتظره در سرور"

    # ارسال پاسخ به بله
    requests.post(
        f"https://tapi.bale.ai/bot{BOT_TOKEN}/sendMessage",
        json={
            "chat_id": chat_id,
            "text": answer
        },
        timeout=10
    )

    return "ok"


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )
