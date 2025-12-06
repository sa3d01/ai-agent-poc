"""Entry point for the AI agent proof‑of‑concept.

This script demonstrates how a simple AI agent can:

* Classify a support ticket using a language model.
* Generate a professional email response.
* Determine a basic remediation plan.
* Execute mock actions based on the ticket intent.

The goal is to showcase the flow end‑to‑end rather than provide a
production‑ready implementation.
"""

import argparse
import json
import os
from typing import Dict, Optional

import openai
from dotenv import load_dotenv

from mock_tools import reset_password, restart_device, unlock_account
from prompts import classification_prompt, email_prompt


def call_llm(prompt: str, text: str) -> str:
    """Call the OpenAI API (or return a mock response) with the given prompt.

    If the environment variable `MOCK_LLM` is set to "1", a fixed string is
    returned instead of calling the real API. Otherwise, the GPT‑4o mini
    endpoint is used.
    """
    # Support mock responses for offline mode or testing without an API key.
    if os.getenv("MOCK_LLM") == "1":
        # Return a simple mock classification response in JSON format
        return "{\"intent\": \"unknown\", \"confidence\": 0.5}"

    # Load the API key and create an OpenAI client.  Starting with v1.0 of the
    # openai‑python library, the `openai.ChatCompletion.create` function has been
    # removed in favor of a client‑based API.  See the migration guide for
    # details: https://github.com/openai/openai-python/discussions/742
    from openai import OpenAI

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY environment variable must be set")
    client = OpenAI(api_key=api_key)

    # Use the new client API to create a chat completion.  We pass the
    # conversation as a list of role/content dictionaries.  The `response`
    # object returns messages as objects, so we access `.message.content`.
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": prompt.strip()},
            {"role": "user", "content": text.strip()},
        ],
    )
    return response.choices[0].message.content


def classify_ticket(ticket: str) -> Dict[str, object]:
    """Classify the ticket and return a JSON with intent and confidence."""
    result = call_llm(classification_prompt, ticket)
    try:
        parsed = json.loads(result)
        return {
            "intent": parsed.get("intent", "unknown"),
            "confidence": float(parsed.get("confidence", 0)),
        }
    except (json.JSONDecodeError, ValueError):
        return {"intent": "unknown", "confidence": 0.0}


def generate_email(ticket: str, intent: str) -> str:
    """Generate a professional email response using an LLM."""
    return call_llm(email_prompt, f"Ticket: {ticket}\nIntent: {intent}")


def plan_actions(intent: str) -> Optional[str]:
    """Return a human‑readable plan for the given intent."""
    # In a real system, this would come from RAG + SOPs. For the demo, it's static.
    if intent == "password_reset":
        return "1) Validate user exists. 2) Call reset_password. 3) Notify user."
    if intent == "vpn_issue":
        return "1) Gather more info on VPN error. 2) Restart device if needed. 3) Escalate if unresolved."
    if intent == "account_locked":
        return "1) Verify identity. 2) Call unlock_account. 3) Advise on security best practices."
    return None


def execute_mock_actions(intent: str) -> Dict[str, object]:
    """Execute one of the mock actions based on intent and return a result."""
    if intent == "password_reset":
        return reset_password("user@example.com")
    if intent == "vpn_issue":
        return restart_device("Laptop-123")
    if intent == "account_locked":
        return unlock_account("user@example.com")
    return {"status": "skipped", "reason": "No mock action defined for intent"}


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the AI agent demo")
    parser.add_argument("--ticket", type=str, help="Ticket text to process")
    parser.add_argument("--file", type=str, help="Path to a file containing the ticket text")
    args = parser.parse_args()

    # Load environment variables from .env if present.
    load_dotenv()

    # Determine the ticket content.
    if args.ticket:
        ticket = args.ticket
    elif args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            ticket = f.read()
    else:
        raise ValueError("Please provide either --ticket or --file")

    print("\n=== Incoming Ticket ===")
    print(ticket)

    # Classify the ticket.
    classification = classify_ticket(ticket)
    print("\n=== Classification ===")
    print(classification)

    # Generate email response.
    email = generate_email(ticket, classification.get("intent", "unknown"))
    print("\n=== Email Response ===")
    print(email)

    # Determine and display a simple action plan.
    plan = plan_actions(classification.get("intent", ""))
    if plan:
        print("\n=== Action Plan ===")
        print(plan)

    # Execute mock action.
    result = execute_mock_actions(classification.get("intent", ""))
    print("\n=== Mock Action Result ===")
    print(result)


if __name__ == "__main__":
    main()
