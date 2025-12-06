"""Entry point for the AI agent proof-of-concept.

This script demonstrates how a simple AI agent can:
* Classify a support ticket using basic keyword heuristics.
* Generate a professional email response.
* Determine a basic remediation plan.
* Execute mock actions based on the ticket intent.

The goal is to showcase the flow end-to-end rather than provide a production-ready implementation.
"""

import argparse
from typing import Dict, List

# Import mock functions
from mock_tools import reset_password, restart_device, unlock_account


def classify_ticket(ticket: str) -> Dict[str, float]:
    """Classify the ticket based on simple keyword heuristics."""
    text = ticket.lower()
    intent = "unknown"
    confidence = 0.5

    if any(word in text for word in ["password", "login", "credential"]):
        intent = "password_reset"
        confidence = 0.9
    elif "vpn" in text:
        intent = "vpn_issue"
        confidence = 0.9
    elif any(word in text for word in ["printer", "printing", "offline"]):
        intent = "printer_error"
        confidence = 0.8
    elif "lock" in text:
        intent = "account_locked"
        confidence = 0.8

    return {"intent": intent, "confidence": confidence}


def generate_email(ticket: str, intent: str) -> str:
    """Generate a simple email response based on the intent."""
    greeting = "Hello,\n\n"
    if intent == "password_reset":
        body = (
            "We have received your request regarding login difficulties. "
            "We are resetting your password and will send instructions shortly."
        )
    elif intent == "vpn_issue":
        body = (
            "We understand you're having trouble connecting to the VPN. "
            "We're running diagnostics and will inform you once resolved."
        )
    elif intent == "printer_error":
        body = (
            "We see that you're experiencing printer issues. "
            "We're working on resolving the connectivity problem."
        )
    elif intent == "account_locked":
        body = (
            "It looks like your account is locked. "
            "We're unlocking it now and will notify you once complete."
        )
    else:
        body = (
            "Thank you for reaching out. We've received your ticket and "
            "will investigate the issue."
        )
    return greeting + body + "\n\nBest regards,\nSupport Team"


def plan_actions(intent: str) -> List[Dict[str, str]]:
    """Return a list of actions to perform based on intent."""
    if intent == "password_reset":
        return [{"step": "Reset user password", "action": "reset_password"}]
    if intent == "vpn_issue":
        return [{"step": "Restart VPN service on user machine", "action": "restart_device"}]
    if intent == "printer_error":
        return [{"step": "Restart printer device", "action": "restart_device"}]
    if intent == "account_locked":
        return [{"step": "Unlock user account", "action": "unlock_account"}]
    return []


def execute_mock_actions(intent: str):
    """Execute mocked actions based on intent."""
    if intent == "password_reset":
        return reset_password("user@example.com")
    if intent == "vpn_issue":
        return restart_device("VPN Client")
    if intent == "printer_error":
        return restart_device("Printer")
    if intent == "account_locked":
        return unlock_account("user@example.com")
    return {"status": "skipped", "reason": "No mock action defined for intent"}


def main():
    parser = argparse.ArgumentParser(
        description="AI agent demo for processing support tickets."
    )
    parser.add_argument("--ticket", type=str, help="Ticket text to process")
    parser.add_argument("--file", type=str, help="Path to text file containing ticket")
    args = parser.parse_args()

    if args.ticket:
        ticket = args.ticket
    elif args.file:
        with open(args.file, "r") as f:
            ticket = f.read()
    else:
        raise SystemExit("Please provide a ticket using --ticket or --file")

    print("=== Incoming Ticket ===")
    print(ticket)
    classification = classify_ticket(ticket)
    print("\n=== Classification ===")
    print(classification)
    email = generate_email(ticket, classification["intent"])
    print("\n=== Email Response ===")
    print(email)
    plan = plan_actions(classification["intent"])
    print("\n=== Action Plan ===")
    print(plan)
    result = execute_mock_actions(classification["intent"])
    print("\n=== Mock Action Result ===")
    print(result)


if __name__ == "__main__":
    main()
