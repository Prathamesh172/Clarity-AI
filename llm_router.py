import requests
import os
import json
import re

# Ollama settings
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "alibayram/medgemma:latest"

# Tavily settings
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
TAVILY_URL = "https://api.tavily.com/search"

# Memory file
MEMORY_FILE = "memory.json"

def load_memory():
    """Load persistent memory from file."""
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return {}

def save_memory(memory):
    """Save persistent memory to file."""
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)

def update_memory(prompt):
    """Extract simple facts from user input and store them."""
    memory = load_memory()

    # Name extraction
    name_match = re.search(r"(?:my name is|i am called)\s+([A-Za-z]+)", prompt, re.I)
    if name_match:
        memory["name"] = name_match.group(1)

    # Age extraction
    age_match = re.search(r"(?:i am|i'm)\s+(\d{1,2})\s*(?:years old|yo)?", prompt, re.I)
    if age_match:
        memory["age"] = age_match.group(1)

    # Location extraction
    location_match = re.search(r"(?:i live in|i'm from)\s+([A-Za-z\s]+)", prompt, re.I)
    if location_match:
        memory["location"] = location_match.group(1).strip()

    save_memory(memory)

def is_search_query(prompt):
    search_keywords = [
        "find", "suggest", "recommend", "near me", "doctor", "therapist",
        "hospital", "clinic", "psychiatrist", "psychologist", "counselor"
    ]
    return any(keyword in prompt.lower() for keyword in search_keywords)

def get_doctor_suggestions(query):
    payload = {
        "api_key": TAVILY_API_KEY,
        "query": query,
        "search_depth": "basic",
        "max_results": 5
    }
    try:
        response = requests.post(TAVILY_URL, json=payload)
        response.raise_for_status()
        data = response.json()

        if not data.get("results"):
            return "Sorry, I couldn't find any relevant results."

        results = data["results"]
        suggestions = "\n\n".join(
            [f"**{i+1}. {r['title']}**\n{r['url']}" for i, r in enumerate(results)]
        )
        return f"Here are some suggestions I found:\n\n{suggestions}"

    except Exception as e:
        return f"⚠️ Error fetching search results: {str(e)}"

def get_response_from_medgemma(chat_history):
    # Load persistent memory
    memory = load_memory()
    memory_text = ""
    if memory:
        mem_parts = [f"{key.capitalize()}: {value}" for key, value in memory.items()]
        memory_text = "Known user details: " + ", ".join(mem_parts) + ". "

    # System / persona prompt
    system_prompt = (
        "You are Clarity AI, a compassionate, empathetic AI therapist. "
        "You offer thoughtful advice, emotional support, diagnosis and practical coping strategies. "
        "Always be warm, understanding, and non-judgmental. "
        "You ONLY respond to general greetings, mental health, therapy, emotional wellbeing, "
        "and personal growth related topics. "
        "You do NOT provide coding help, math solutions, or unrelated factual answers. "
        "Always respond warmly, in a supportive and understanding tone."
        f"{memory_text}"
    )

    # Build conversation string
    conversation_text = system_prompt + "\n\n"
    for msg in chat_history:
        role = "User" if msg["role"] == "user" else "Therapist"
        conversation_text += f"{role}: {msg['content']}\n"
    conversation_text += "Therapist:"

    payload = {
        "model": MODEL_NAME,
        "prompt": conversation_text,
        "stream": False
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        data = response.json()
        return data.get("response", "").strip()
    except requests.exceptions.RequestException as e:
        return f"⚠️ Error connecting to Ollama: {str(e)}"

def route_message(prompt, chat_history):
    update_memory(prompt)  # update stored facts
    if is_search_query(prompt):
        return get_doctor_suggestions(prompt)
    return get_response_from_medgemma(chat_history)
