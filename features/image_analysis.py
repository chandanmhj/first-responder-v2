"""
features/image_analysis.py
Downloads image from Telegram and sends to Groq vision model for analysis.
"""

import os
import base64
import requests
from dotenv import load_dotenv
load_dotenv()

from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

VISION_PROMPT = """You are a first aid assistant analyzing an image sent by a bystander during a medical emergency.
Describe what you see in the image in terms of:
1. The apparent condition of the person (conscious/unconscious, breathing, visible injuries, skin color, posture)
2. Any visible wounds, burns, bleeding, or deformities
3. The environment (indoors/outdoors, any hazards visible)

Be factual, calm, and concise. Do NOT make a diagnosis. This description will be used to give first aid guidance."""


def analyze_image_from_telegram(file_path: str, bot_token: str) -> str:
    """
    Download image from Telegram file path and analyze with Groq vision.
    """
    try:
        url = f"https://api.telegram.org/file/bot{bot_token}/{file_path}"
        response = requests.get(url, timeout=15)
        if response.status_code != 200:
            return ""

        image_data = base64.standard_b64encode(response.content).decode("utf-8")
        content_type = "image/jpeg"

        completion = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{content_type};base64,{image_data}"
                            },
                        },
                        {
                            "type": "text",
                            "text": VISION_PROMPT,
                        },
                    ],
                }
            ],
            max_tokens=400,
            temperature=0.2,
        )

        return completion.choices[0].message.content.strip()

    except Exception as e:
        print(f"[IMAGE ANALYSIS ERROR] {e}")
        return ""
