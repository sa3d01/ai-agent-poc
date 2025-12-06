import argparse
import json
import os
import openai
from dotenv import load_dotenv

from prompts import classification_prompt, email_prompt
from mock_tools import reset_password, restart_device, unlock_account

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def call_llm(prompt, text):
    if os.getenv("MOCK_LLM") == "1":
        return "Mock AI Response"
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message["content"]


def classify_ticket(ticket):
    result = call_llm(classification_prompt, ticket)
    try:
        return json.loads(result)
    except:
        return {"intent": "unknown", "confidence": 0.3}


def generate_email(ticket, intent):
    return call_llm(email_prompt, f"Ticket: {ticket}\nIntent: {intent}")


def execute_mock_actions(intent):
    if intent == "password_reset":
        return reset_password("user@example.com")
    if intent == "vpn_issue":
        return restart_device("Laptop-123")
    if intent == "account_locked":
        return unlock_account("user@example.com")
    return {"status": "skipped", "reason": "No matching action"}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ticket", type=str)
    parser.add_argument("--file", type=str)
    args = parser.parse_args()

    if args.ticket:
        ticket = args.ticket
    elif args.file:
        ticket = open(args.file).read()
    else:
        raise Exception("Provide --ticket or --file")

    print("\n=== Incoming Ticket ===")
    print(ticket)

    classification = classify_ticket(ticket)
    print("\n=== Classification ===")
    print(classification)

    email = generate_email(ticket, classification.get("intent"))
    print("\n=== Email Response ===")
    print(email)

    result = execute_mock_actions(classification.get("intent"))
    print("\n=== Mock Action Result ===")
    print(result)


if __name__ == "__main__":
    main()
