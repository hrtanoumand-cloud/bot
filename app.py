from flask import Flask, request
import requests
import os
from urllib.parse import quote

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

WELCOME_TEXT = """
👋 سلام به ربات پیگیری صدای همکار خوش آمدید. 😊

کافیست کد پیگیری خود را که در انتهای ارسال پیام در سامانه صدای همکار ارائه می گردد را ارسال نمایید تا از نتیجه درخواست خود و پیگیری انجام شده مطلع شوید. 😉

در صورتیکه با پیغام خطا مواجه شدید در روزهای آتی مجدد اقدام به استعلام نمایید. موضوع شما در دست پیگیری است و پس از حصول نتیجه جواب مقتضی بارگزاری خواهد شد. 👌☺️
"""

@app.route("/", methods=["POST"])
def webhook():
    data = request.json

    if not data or "message" not in data:
        return "ok"

    chat_id = data["message"]["chat"]["id"]
    user_text = data["message"].get("text", "").strip()

    if not user_text:
        return "ok"

    # مدیریت دستور start
    if user_text == "/start":
        requests.post(
            f"https://tapi.bale.ai/bot{BOT_TOKEN}/sendMessage",
            json={
                "chat_id": chat_id,
                "text": WELCOME_TEXT
            }
        )
        return "ok"

    # جستجو در دیتابیس
    query = quote(user_text)
    url = f"{SUPABASE_URL}/rest/v1/responses?keyword=ilike.{query}&select=answer"

    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Accept": "application/json"
    }

    answer = "❌ عبارتی با این متن پیدا نشد"

    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 200:
            result = r.json()
            if isinstance(result, list) and len(result) > 0:
                answer = result[0].get("answer", answer)
        else:
            answer = "❌ خطا در ارتباط با دیتابیس"
    except Exception:
        answer = "❌ خطای سرور"

    requests.post(
        f"https://tapi.bale.ai/bot{BOT_TOKEN}/sendMessage",
        json={
            "chat_id": chat_id,
            "text": answer
        }
    )

    return "ok"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))