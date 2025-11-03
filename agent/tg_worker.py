# tg_worker.py
import os
import time
import requests

TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
GL1TCH_API_URL = os.environ.get("GL1TCH_API_URL", "").rstrip("/")
API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

def send_message(chat_id, text):
    requests.post(f"{API_URL}/sendMessage", json={"chat_id": chat_id, "text": text})

def handle_message(chat_id, text):
    try:
        res = requests.post(f"{GL1TCH_API_URL}/glitch", json={"prompt": text}, timeout=20)
        res.raise_for_status()
        data = res.json()
        reply = data.get("response", "No response from GL1TCH")
    except Exception as e:
        reply = f"⚠️ Error: {e}"
    send_message(chat_id, reply)

def main():
    offset = None
    print("🤖 Telegram worker started...")
    while True:
        try:
            resp = requests.get(f"{API_URL}/getUpdates", params={"timeout": 50, "offset": offset}, timeout=60)
            resp.raise_for_status()
            updates = resp.json().get("result", [])
            for upd in updates:
                offset = upd["update_id"] + 1
                msg = upd.get("message")
                if not msg:
                    continue
                chat_id = msg["chat"]["id"]
                text = msg.get("text", "")
                if text:
                    handle_message(chat_id, text)
        except Exception as e:
            print("Worker error:", e)
            time.sleep(2)

if __name__ == "__main__":
    main()