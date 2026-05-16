# Jeeva — First Aid Telegram Bot 🚑

An AI-powered Telegram bot that provides step-by-step BCLS (Basic Cardiac Life Support) first aid guidance during medical emergencies. Built by **Chandan and team from Sambhram Institute of Technology, Bangalore**.

---

## Features

| Feature | Tech |
|---|---|
| Telegram messaging | python-telegram-bot + FastAPI webhook |
| Conversational AI | Groq LLM (LLaMA 3.3 70B) |
| Image analysis | Groq Vision (LLaMA 4 Scout Vision) |
| BCLS protocol RAG | ChromaDB + sentence-transformers |
| Auto media per step | Images/videos sent for key first aid steps |
| Session memory | In-memory per chat ID |

---

## Project Structure

```
jeeva-telegram-bot/
│
├── main.py                        # FastAPI app, Telegram /webhook
├── requirements.txt
├── Procfile                       # For Koyeb/Railway deployment
├── .env                           # Your API keys (never commit)
├── .env.example
├── .gitignore
│
├── features/
│   ├── conversation.py            # Groq LLM + RAG + step tag parser
│   ├── rag.py                     # ChromaDB query
│   ├── image_analysis.py          # Groq vision for patient images
│   └── media_map.py               # Maps scenario+step to media file
│
├── knowledge_base/
│   ├── data.py                    # 11 BCLS scenarios, 63 chunks
│   ├── ingest.py                  # Embed and store in ChromaDB (run once)
│   └── chroma_db/                 # Auto-created after ingest
│
├── media/
│   ├── README.md                  # ← MEDIA NAMING GUIDE (read this!)
│   └── (your images and videos go here)
│
└── utils/
    └── session_store.py           # Per-chat conversation history
```

---

## Setup Instructions

### 1. Create your Telegram bot

- Open Telegram → search **@BotFather**
- Send `/newbot`
- Name: `Jeeva` → Username: `JeevaFirstAidBot`
- Copy the token BotFather gives you

### 2. Install dependencies

```bash
pip install -r requirements.txt
pip install tf-keras
```

### 3. Configure .env

```env
TELEGRAM_BOT_TOKEN=your_token_here
TELEGRAM_BOT_USERNAME=JeevaFirstAidBot
GROQ_API_KEY=your_groq_key_here
PORT=8000
```

### 4. Add media files (optional but recommended)

- Read `media/README.md` for exact filenames
- Add your images/videos to the `media/` folder
- Bot will automatically send media after relevant steps

### 5. Ingest knowledge base (run once)

```bash
python knowledge_base/ingest.py
```

### 6. Run the server

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 7. Expose with ngrok (local testing)

```bash
ngrok http 8000
```

### 8. Register Telegram webhook

Open this URL in your browser (replace with your ngrok URL):

```
https://your-ngrok-url/set-webhook?url=https://your-ngrok-url
```

You should see: `{"status": "webhook set"}`

### 9. Test it

Open Telegram → search your bot → send any message:
- `Hi` — greeting
- `Someone collapsed and isn't breathing` — cardiac arrest guidance
- `My friend is having a seizure` — seizure guidance
- Send a photo of an injured person — image analysis + guidance

---

## Deployment on Koyeb (Free, never sleeps)

1. Push to GitHub (`.env` and `media/` are gitignored)
2. Go to [koyeb.com](https://koyeb.com) → New App → GitHub
3. Select your repo
4. Set environment variables (same as `.env`)
5. Start command is already in `Procfile`
6. Koyeb gives you a public URL like `https://jeeva-bot.koyeb.app`
7. Register webhook:
```
https://jeeva-bot.koyeb.app/set-webhook?url=https://jeeva-bot.koyeb.app
```

**Note:** Media files won't persist on Koyeb's free tier. For media to work in production, host files on Cloudinary or similar and update `media_map.py` to use URLs instead of file paths.

---

## How It Works

```
User sends Telegram message
        ↓
Telegram forwards to /webhook (FastAPI)
        ↓
If photo → Groq Vision analyzes patient image
        ↓
Message + image description → ChromaDB RAG query
        ↓
Relevant BCLS steps retrieved
        ↓
Groq LLaMA 3.3 70B generates reply with [STEP:scenario:number] tag
        ↓
Tag parsed → text sent to user → media sent if available for that step
```

---

## BCLS Knowledge Base

**Source:** JeevaRaksha Trust BCLS Provider Handbook, 2nd Edition, January 2025

| Scenario | Steps |
|---|---|
| Scene Safety & Primary Assessment | 8 |
| Heart Attack | 7 |
| Stroke | 4 |
| Fits / Seizures | 6 |
| Low Blood Sugar | 4 |
| Snake Bite | 6 |
| Trauma / Road Accident | 8 |
| Burns | 3 |
| Cardiac Arrest / CPR | 11 |
| Choking | 7 |
| Infections / Animal Bites | 2 |

---

## Media Files

See `media/README.md` for the complete list of filenames and what each should show.

---

*Built by Chandan and team — Sambhram Institute of Technology, Bangalore*
