# agent_manager.py – Backend manager for IsaKaiHBG_AI

import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from core import router  # Connect to router.py

class AgentManager:
    def __init__(self):
        self.demo_mode = True  # Start with Demo Mode ON

    def toggle_mode(self):
        self.demo_mode = not self.demo_mode
        return "Demo Mode (ON)" if self.demo_mode else "Real Mode (ON)"

    def handle_input(self, user_text: str) -> str:
        """Return either a stubbed response or call real router logic."""
        if self.demo_mode:
            text = user_text.lower()
            if "gemma" in text or "summarize" in text:
                return "[Gemma Stub] Summarizing funding trends..."
            elif "wizard" in text or "script" in text:
                return "[WizardCoder Stub] Generating trading script..."
            elif "mistral" in text or "plan" in text:
                return "[Mistral Stub] Suggesting $75 prop firm plan..."
            elif "pitch deck" in text or "funding" in text:
                return "[Stub] Simulating pitch deck generation..."
            else:
                return f"[Stub AI] I heard: {user_text}"
        else:
            try:
                return router.handle_query(user_text)
            except Exception as e:
                return f"[Error] {str(e)}"
