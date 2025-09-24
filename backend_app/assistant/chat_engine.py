"""
Module: chat_engine
Defines the chat interface for the AI assistant.
"""

from typing import Dict, Any
import os
from openai import OpenAI

# Initialize OpenAI client (requires OPENAI_API_KEY in your environment)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def process_user_input(user_input: str, context: Dict[str, Any] | None = None) -> str:
    """
    Process the user's input and return an appropriate response from the AI model.

    Args:
        user_input (str): The user's question or statement.
        context (Dict[str, Any], optional): Additional context for the conversation.

    Returns:
        str: The assistant's response.
    """
    try:
        messages = [{"role": "user", "content": user_input}]
        if context:
            messages.insert(0, {"role": "system", "content": f"Context: {context}"})

        completion = client.chat.completions.create(
            model="gpt-4o-mini",  # lightweight GPT-4 optimized model
            messages=messages,
            max_tokens=300
        )

        response = completion.choices[0].message.content
        return response.strip()

    except Exception as e:
        return f"[Error in chat_engine: {e}]"
