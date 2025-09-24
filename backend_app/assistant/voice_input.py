"""
Module: voice_input
Handles speech-to-text for user queries.
"""

import os
from openai import OpenAI

# Initialize OpenAI client (requires OPENAI_API_KEY in your environment)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def transcribe_audio(audio_file_path: str) -> str:
    """
    Transcribe audio to text using OpenAI Whisper.

    Args:
        audio_file_path (str): Path to the audio file.

    Returns:
        str: Transcribed text.
    """
    try:
        with open(audio_file_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model="whisper-1",  # OpenAI Whisper model
                file=audio_file
            )
        return transcription.text.strip()
    except Exception as e:
        return f"[Error in voice_input: {e}]"
