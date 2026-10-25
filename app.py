import io
import os
import json
import datetime
import streamlit as st
import ollama
from gtts import gTTS
from PIL import Image

# Directory for saving feedback locally on disk
FEEDBACK_DIR = "feedback_data"
FEEDBACK_FILE = os.path.join(FEEDBACK_DIR, "corrections.json")

if not os.path.exists(FEEDBACK_DIR):
    os.makedirs(FEEDBACK_DIR)

if not os.path.exists(FEEDBACK_FILE):
    with open(FEEDBACK_FILE, "w") as f:
        json.dump([], f)

def save_feedback(image, caption, feedback_type):
    """Saves user feedback and image permanently to hard disk."""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    img_filename = f"img_{timestamp}.jpg"
    img_path = os.path.join(FEEDBACK_DIR, img_filename)

    # Fix for RGBA/transparent image saving error
    if image.mode in ("RGBA", "P"):
        image = image.convert("RGB")
    image.save(img_path)

    with open(FEEDBACK_FILE, "r") as f:
        records = json.load(f)

    records.append({
        "timestamp": timestamp,
        "image_path": img_path,
        "caption": caption,
        "feedback": feedback_type
    })

    with open(FEEDBACK_FILE, "w") as f:
        json.dump(records, f, indent=4)

def generate_caption_ollama(image, custom_instruction=""):
    """Sends image to local LLaVA via Ollama and returns a description."""
    temp_path = "temp_input.jpg"
    if image.mode != "RGB":
        image = image.convert("RGB")
    image.save(temp_path)

    # Detailed system prompt tailored specifically for LLaVA
    prompt = (
        "You are an assistive vision guide for a visually impaired person. "
        "Describe this image naturally and clearly in 2-3 sentences. "
        "Focus on: "
        "1. Main objects or people and their spatial positions (left, right, center, in front). "
        "2. Any immediate obstacles or hazards on the ground. "
        "3. Read any visible text or labels if present."
    )

    if custom_instruction:
        prompt += f"\nNote: {custom_instruction}"

    response = ollama.chat(
        model="llava",
        messages=[{
            'role': 'user',
            'content': prompt,
            'images': [temp_path]
        }],
        options={
            "temperature": 0.2  # Keep description factual and consistent
        }
    )
    
    return response['message']['content']

def text_to_audio(caption):
    audio_buffer = io.BytesIO()
    tts = gTTS(text=caption, lang="en")
    tts.write_to_fp(audio_buffer)
    audio_buffer.seek(0)
    return audio_buffer.getvalue()