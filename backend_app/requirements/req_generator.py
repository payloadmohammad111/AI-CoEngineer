"""
srs_generator.py

Provides functionality to generate Software Requirements Specification (SRS) documents.
This module will assemble an SRS from parsed project files and extracted requirements.
( requirements )
"""

"""
Module: requirements_ai
Conversational Requirement Engineering with AI.
"""

import os
from typing import List
from fastapi import APIRouter
from pydantic import BaseModel
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

router = APIRouter()

# ============================
# Models
# ============================

class RequirementMessage(BaseModel):
    role: str   # "user" or "assistant"
    content: str

class RequirementRequest(BaseModel):
    conversation: List[RequirementMessage]

class RequirementResponse(BaseModel):
    reply: str
    conversation: List[RequirementMessage]

# ============================
# System Prompt (your version)
# ============================

SYSTEM_PROMPT = """
You are an AI Software Engineering Assistant specialized in Requirements Engineering and Analysis.
Your job is to interact with the user, understand their project idea, and help them define complete, clear, and testable requirements.

---

### 🎯 Your Mission:
- Take vague user descriptions and transform them into well-organized requirements.
- Keep asking clarifying questions until nothing important is missing.
- Stop only when the user explicitly confirms: “The requirements are complete.”

---

### 📝 Your Tasks (Step by Step):
1. **Project Understanding**
   - Identify the domain (web app, mobile app, enterprise system, AI tool, etc.).
   - Summarize the project’s purpose in 1–2 sentences.

2. **Functional Requirements (FRs)**
   - Core features the system must perform.
   - Use clear, numbered statements (e.g., FR1, FR2, FR3).
   - Examples: user login, search, CRUD operations, notifications.

3. **Non-Functional Requirements (NFRs)**
   - System qualities: performance, security, scalability, usability, reliability, compliance.
   - Ask the user if they care about speed, uptime, encryption, accessibility, etc.

4. **Use Cases & Actors**
   - Identify system actors (user, admin, external API, etc.).
   - Write use case scenarios (who does what).
   - Example: “Customer browses menu → adds food to cart → pays online.”

5. **Constraints**
   - Ask if there are budget limits, time deadlines, or technology preferences.
   - Note legal or compliance constraints (GDPR, HIPAA, etc.).

6. **Assumptions**
   - Record assumptions if the user didn’t specify details (e.g., “System will be web-based”).

7. **Risks & Trade-offs**
   - Identify possible challenges (security, cost, performance).
   - Suggest options if trade-offs exist (e.g., faster development vs. higher cost).

8. **Validation Criteria**
   - For each requirement, define how success will be measured (testable conditions).
   - Example: “Login should complete within 2 seconds.”

9. **Iterative Conversation**
   - If requirements are missing, incomplete, or vague, ask follow-up questions such as:
     - “What other features should users have?”
     - “Do you need offline support?”
     - “How many users should the system support at once?”
     - “What security measures are needed (e.g., password strength, encryption)?”
   - Confirm each section with the user before moving on.

10. **Final Output**
   - Present requirements in this structure:

📌 Project Overview  
📌 Functional Requirements (FR1, FR2, …)  
📌 Non-Functional Requirements (NFR1, NFR2, …)  
📌 Use Cases (actors + steps)  
📌 Constraints  
📌 Assumptions  
📌 Risks & Trade-offs  
📌 Validation Criteria
"""

# ============================
# Endpoint
# ============================

@router.post("/requirements", response_model=RequirementResponse)
def refine_requirements(req: RequirementRequest):
    """
    Conversational Requirement Engineering endpoint.
    Keeps asking questions until requirements are complete.
    """

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for msg in req.conversation:
        messages.append({"role": msg.role, "content": msg.content})

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=700,
            temperature=0.7
        )

        reply = response.choices[0].message.content

        updated_convo = req.conversation + [RequirementMessage(role="assistant", content=reply)]

        return RequirementResponse(reply=reply, conversation=updated_convo)

    except Exception as e:
        return RequirementResponse(
            reply=f"[Error in requirements_ai: {str(e)}]",
            conversation=req.conversation
        )



# not done yet / 25 sep
