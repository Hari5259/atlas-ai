"""
Configuration for Atlas AI
"""

# Conversational AI Config
CONVERSATIONAL_CONFIG = {
    "enabled": True,
    "response_delay": 0,  # milliseconds
    "use_emoji": True,
    "personality": "friendly",
    "remember_names": True,
    "history_size": 100,
}

# Ollama Config
OLLAMA_CONFIG = {
    "base_url": "http://localhost:11434",
    "chat_model": "llama3",
    "embedding_model": "nomic-embed-text",
    "timeout": 60,
}

# ChromaDB Config
CHROMADB_CONFIG = {
    "persist_directory": "./data",
    "collection_name": "documents",
    "auto_create": True,
}

# API Config
API_CONFIG = {
    "host": "0.0.0.0",
    "port": 8000,
    "debug": False,
    "cors_origins": ["*"],
}

# Response Config
RESPONSE_CONFIG = {
    "max_retries": 3,
    "fallback_to_conversational": True,
    "show_response_type": True,
    "include_metadata": True,
}
