from chromadb import Client
from chromadb.config import Settings

# Initialize Chroma in local persistent mode
client = Client(Settings(
    persist_directory="~/NCPrime/IsaKaiHBG_AI/memory/chroma_store"
))

collection = client.get_or_create_collection("isa_memory")

def store_memory(text):
    """
    Store a text snippet in vector memory.
    """
    collection.add(documents=[text], ids=[str(hash(text))])

def get_relevant_memories(query, n_results=5):
    """
    Retrieve top n relevant memories based on similarity.
    """
    results = collection.query(query_texts=[query], n_results=n_results)
    return results["documents"]

def get_recent_memories(n_results=3):
    """
    Fetch most recent stored memories.
    """
    all_docs = collection.get()
    docs = list(all_docs["documents"])
    return docs[-n_results:] if len(docs) >= n_results else docs
