"""
Module: voice_output
Handles text-to-speech for assistant responses.
"""

import os
from pathlib import Path
from openai import OpenAI

# Initialize OpenAI client (requires OPENAI_API_KEY in your environment)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def speak_text(text: str, output_file: str | None = None) -> str:
    """
    Convert text to speech and optionally save to an audio file.

    Args:
        text (str): The text to convert to speech.
        output_file (str, optional): Path to save the audio file (default: output.mp3)

    Returns:
        str: Path to the generated audio file.
    """
    try:
        if output_file is None:
            output_file = "output.mp3"

        speech_file_path = Path(output_file)

        response = client.audio.speech.create(
            model="gpt-4o-mini-tts",   # OpenAI text-to-speech model
            voice="alloy",             # Available voices: alloy, verse, etc.
            input=text
        )

        with open(speech_file_path, "wb") as f:
            f.write(response.read())

        return str(speech_file_path)

    except Exception as e:
        return f"[Error in voice_output: {e}]"
