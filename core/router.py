import subprocess

def run_ollama(model: str, prompt: str) -> str:
    """Call Ollama locally to query a specific model."""
    try:
        result = subprocess.run(
            ["ollama", "run", model],
            input=prompt.encode(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=60
        )
        return result.stdout.decode().strip() or "[No response from Ollama]"
    except Exception as e:
        return f"[Ollama Error: {e}]"

def handle_query(user_input: str) -> str:
    """Route queries to appropriate Ollama models."""
    text = user_input.lower()
    if "gemma" in text or "summarize" in text:
        return run_ollama("gemma", user_input)
    elif "wizard" in text or "code" in text or "script" in text:
        return run_ollama("wizardcoder", user_input)
    else:
        return run_ollama("mistral", user_input)  # Default model
