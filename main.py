"""
main.py
FastAPI app — Telegram webhook for Jeeva First Aid Bot.
Handles text, images, inline buttons, and ambulance arrival summary.
"""

import os
import requests
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Request
from fastapi.responses import Response
from features.media_map import get_media_path, get_cached_file_id, cache_file_id

from features.conversation import get_bot_reply
from features.image_analysis import analyze_image_from_telegram
from features.media_map import get_media_path
from utils.session_store import add_message, get_history, clear_session

app = FastAPI(title="Jeeva First Aid Telegram Bot")

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

# ── Keywords that trigger ambulance arrival summary ───────────────────────────
ARRIVAL_KEYWORDS = [
    "ambulance arrived", "ambulance is here", "help arrived", "paramedics arrived",
    "doctor arrived", "rescue arrived", "emergency team arrived", "ambulance reached",
    "108 arrived", "they arrived", "rescue team is here", "medics arrived"
]

# ── Step confirmation buttons ─────────────────────────────────────────────────
STEP_BUTTONS = [
    [
        {"text": "✅ Step done, next please", "callback_data": "step_done"},
        {"text": "❌ Step didn't work", "callback_data": "step_failed"},
    ]
]

# ── Telegram API helpers ──────────────────────────────────────────────────────

def send_message(chat_id: int, text: str, with_buttons: bool = False):
    url = f"{TELEGRAM_API}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown",
    }
    if with_buttons:
        payload["reply_markup"] = {"inline_keyboard": STEP_BUTTONS}
    r = requests.post(url, json=payload)
    print(f"[SENT TEXT] Status: {r.status_code}")


def send_photo(chat_id: int, photo_path: str, caption: str = ""):
    filename = os.path.basename(photo_path)
    cached_id = get_cached_file_id(filename)

    if cached_id:
        # Send instantly using file_id
        requests.post(f"{TELEGRAM_API}/sendPhoto", json={
            "chat_id": chat_id,
            "photo": cached_id,
            "caption": caption
        })
    else:
        # Upload and cache the returned file_id
        url = f"{TELEGRAM_API}/sendPhoto"
        with open(photo_path, "rb") as f:
            r = requests.post(url, files={"photo": f}, data={"chat_id": chat_id, "caption": caption})
        result = r.json().get("result", {})
        file_id = result.get("photo", [{}])[-1].get("file_id")
        if file_id:
            cache_file_id(filename, file_id)


def send_video(chat_id: int, video_path: str, caption: str = ""):
    filename = os.path.basename(video_path)
    cached_id = get_cached_file_id(filename)

    if cached_id:
        # Send instantly using file_id
        requests.post(f"{TELEGRAM_API}/sendVideo", json={
            "chat_id": chat_id,
            "video": cached_id,
            "caption": caption
        })
    else:
        # Upload and cache the returned file_id
        url = f"{TELEGRAM_API}/sendVideo"
        with open(video_path, "rb") as f:
            r = requests.post(url, files={"video": f}, data={"chat_id": chat_id, "caption": caption})
        result = r.json().get("result", {})
        file_id = result.get("video", {}).get("file_id")
        if file_id:
            cache_file_id(filename, file_id)

def send_typing(chat_id: int):
    requests.post(f"{TELEGRAM_API}/sendChatAction", json={
        "chat_id": chat_id,
        "action": "typing"
    })


def answer_callback(callback_query_id: str, text: str = ""):
    requests.post(f"{TELEGRAM_API}/answerCallbackQuery", json={
        "callback_query_id": callback_query_id,
        "text": text,
    })


def get_file_path(file_id: str) -> str:
    r = requests.get(f"{TELEGRAM_API}/getFile", params={"file_id": file_id})
    return r.json().get("result", {}).get("file_path", "")


def set_webhook(webhook_url: str):
    r = requests.post(f"{TELEGRAM_API}/setWebhook", json={"url": webhook_url})
    print(f"[WEBHOOK SET] {r.json()}")


def is_arrival_message(text: str) -> bool:
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in ARRIVAL_KEYWORDS)


def build_paramedic_summary(chat_id: str) -> str:
    """Build a summary of the emergency from conversation history."""
    history = get_history(str(chat_id))
    if not history:
        return "No prior conversation history available."

    # Extract key info from conversation
    summary_lines = []
    for msg in history:
        if msg["role"] == "user":
            summary_lines.append(f"Bystander: {msg['content']}")

    conversation_text = "\n".join(summary_lines[:10])  # Last 10 user messages

    # Ask Groq to summarize for paramedics
    from groq import Groq
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """You are a medical assistant. Based on the bystander conversation below, 
                create a brief, clear handover summary for arriving paramedics. Include:
                - What happened (incident type)
                - Victim's current condition as reported
                - First aid steps already performed
                - Any medications given
                Keep it under 150 words. Use bullet points. Be clinical and clear."""
            },
            {
                "role": "user",
                "content": f"Bystander conversation:\n{conversation_text}"
            }
        ],
        max_tokens=300,
        temperature=0.2,
    )
    return response.choices[0].message.content.strip()


# ── Process incoming message ──────────────────────────────────────────────────

async def handle_message(message: dict):
    chat_id = message["chat"]["id"]
    user_message = ""
    image_description = ""

    if "text" in message:
        user_message = message["text"].strip()
    elif "photo" in message:
        caption = message.get("caption", "")
        user_message = caption if caption else "I sent you an image of a patient. Please assess."
        photo = message["photo"][-1]
        file_path = get_file_path(photo["file_id"])
        if file_path:
            image_description = analyze_image_from_telegram(file_path, BOT_TOKEN)
    else:
        send_message(chat_id, "Sorry, I can only process text messages and images right now.")
        return

    print(f"[MESSAGE] Chat: {chat_id} | Text: {user_message}")

    # ── Ambulance/help arrival detection ─────────────────────────────────
    if is_arrival_message(user_message):
        send_typing(chat_id)
        summary = build_paramedic_summary(str(chat_id))
        handover = (
            "🚑 *Paramedic Handover Summary*\n\n"
            f"{summary}\n\n"
            "---\n"
            "✅ *Professional help has arrived. You did great!*\n"
            "The patient is now in safe hands. Stay calm and cooperate with the paramedics.\n\n"
            "_Jeeva — BCLS First Aid Bot by Chandan and team, Sambhram Institute of Technology_"
        )
        send_message(chat_id, handover)
        clear_session(str(chat_id))
        return

    send_typing(chat_id)
    add_message(str(chat_id), "user", user_message)

    reply, scenario, step = get_bot_reply(
        chat_id=str(chat_id),
        user_message=user_message,
        image_description=image_description,
    )

    add_message(str(chat_id), "assistant", reply)

    # Show buttons only when guiding through emergency steps
    show_buttons = scenario is not None
    send_message(chat_id, reply, with_buttons=show_buttons)

    # Send media if available
    if scenario and step:
        media_path, media_type = get_media_path(scenario, step)
        if media_path:
            print(f"[MEDIA] Sending {media_type}: {media_path}")
            if media_type == "photo":
                send_photo(chat_id, media_path)
            elif media_type == "video":
                send_video(chat_id, media_path)


# ── Handle button callbacks ───────────────────────────────────────────────────

async def handle_callback(callback_query: dict):
    chat_id = callback_query["message"]["chat"]["id"]
    callback_id = callback_query["id"]
    data = callback_query.get("data", "")

    answer_callback(callback_id)

    if data == "step_done":
        await handle_message({
            "chat": {"id": chat_id},
            "text": "Done, next step please"
        })

    elif data == "step_failed":
        await handle_message({
            "chat": {"id": chat_id},
            "text": "This step didn't work, what should I do next?"
        })

# ── Routes ────────────────────────────────────────────────────────────────────

@app.get("/")
def health_check():
    return {"status": "ok", "bot": "Jeeva First Aid Telegram Bot"}


@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    print(f"[INBOUND] {data}")

    try:
        # Handle button press
        if "callback_query" in data:
            await handle_callback(data["callback_query"])
            return Response(content="", status_code=200)

        # Handle message
        message = data.get("message") or data.get("edited_message")
        if not message:
            return Response(content="", status_code=200)

        await handle_message(message)

    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()

    return Response(content="", status_code=200)


@app.get("/set-webhook")
def register_webhook(url: str):
    set_webhook(f"{url}/webhook" if not url.endswith("/webhook") else url)
    return {"status": "webhook set", "url": url}