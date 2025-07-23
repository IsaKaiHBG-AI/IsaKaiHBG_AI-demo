def store_memory(text):
    print(f"[Memory] Stored: {text}")

def get_relevant_memories(query):
    return [f"Relevant memory for: {query}"]

def get_recent_memories(count=3):
    return [f"Recent memory {i}" for i in range(count)]
