"""
Minimal main_agent.py for Hugging Face Space.

This file exposes a single entrypoint function:

    run_agent(user_input: str) -> str

You can later replace the internals with your real multi-agent logic.
"""

from typing import Dict


class MainAgent:
    """
    Placeholder MainAgent.

    Replace the handle_message method with your real
    multi-agent pipeline (planner → workers → evaluator, etc.).
    """

    def handle_message(self, user_input: str) -> Dict[str, str]:
        # TODO: replace this stub with real logic
        reply = f"Echo from MainAgent: {user_input}"
        return {"response": reply}


def run_agent(user_input: str) -> str:
    """
    Entry point used by app.py (and Hugging Face Spaces).

    It must accept a single string and return a single string.
    """
    agent = MainAgent()
    result = agent.handle_message(user_input)
    return result["response"]
