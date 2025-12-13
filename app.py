from flask import Flask, request
import requests
import os

app = Flask(__name__)

# متغیرهای محیطی (در Render تنظیم شده‌اند)
BOT_TOKEN = os.getenv("BOT_TOKEN")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


@app.route("/", methods=["POST"])
def webhook():
    data = request.json

    # اگر پیام معمولی نبود (مثلاً callback)، کاری نکن
    if not data or "message" not in data:
        return "ok"

    chat_id = data["message"]["chat"]["id"]
    user_text = data["message"].get("text", "").strip()

    # اگر کاربر متن نفرستاده
    if not user_text:
        return "ok"

    # درخواست به Supabase
    url = f"{SUPABASE_URL}/rest/v1/responses?keyword=eq.{user_text}"

    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json"
    }

    try:
        r = requests.get(url, headers=headers, timeout=10)
        result = r.json()
    except Exception:
        answer = "❌ خطا در اتصال به دیتابیس"
    else:
        if result:
            answer = result[0].get("answer", "❌ جواب پیدا نشد")
        else:
            answer = "❌ عبارتی با این متن پیدا نشد"

    # ارسال پیام به بله
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
