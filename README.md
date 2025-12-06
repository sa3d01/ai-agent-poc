# AI Agent Demo (POC)

This repository demonstrates a minimal Proof‑of‑Concept for:

1. Generating AI‑driven email responses based on support tickets.
2. Simulating how an AI agent processes incoming tickets.
3. Executing 2–3 mock "actions" that represent automated remediation steps.

This is **not** a production system. It's a lightweight simulation for evaluation purposes.

## 🚀 How It Works

Run the script from the command line and provide a ticket description:

```
python main.py --ticket "User cannot login to Office 365"
```

The agent will:

1. Classify the ticket.
2. Generate an email response.
3. Generate a simple action plan.
4. Execute mock actions.

Everything is printed in the console for easy review.

## 👡 Mock Actions Included

The following functions simulate actions that a real agent might perform. They do not actually perform any changes:

- `reset_password(username)`
- `restart_device(device)`
- `unlock_account(username)`

## 🗁 Folder Structure

```
ai-agent-poc/
  main.py              # runs the full flow
  mock_tools.py        # simulated actions
  prompts.py           # LLM prompts for classification & email
  sample_tickets/      # example inputs
  requirements.txt     # Python package requirements
  README.md
```

## 📦 Installation

Use Python 3.9 or newer. Install dependencies with pip:

```
pip install -r requirements.txt
```

## ▶️ Run Demo

Using an inline ticket:

```
python main.py --ticket "VPN is not connecting for user Ahmed"
```

Or using a file:

```
python main.py --file sample_tickets/password_reset.txt
```

## 🤔 Requirements

- Python 3.9+
- OpenAI API key (set `OPENAI_API_KEY` in your environment). If `MOCK_LLM=1` is set, the script will skip calling the real API and return mock responses.

## 📞 Contact

This PoC is part of the Alphora Agent 101 case study submission.
