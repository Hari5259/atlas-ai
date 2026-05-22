"""
API documentation for Atlas AI endpoints
"""

API_DOCS = {
    "chat": {
        "endpoint": "POST /api/chat",
        "description": "Send a message and receive a response (conversational or knowledge-based)",
        "request": {
            "prompt": "str - User message",
            "model": "str - LLM model (default: llama3)",
            "use_context": "bool - Use knowledge base (default: true)",
        },
        "response": {
            "response": "str - AI response",
            "response_type": "str - 'conversational' or 'knowledge_based'",
            "used_context": "bool - Whether knowledge base was used",
            "context_docs": "int - Number of documents retrieved",
        },
        "examples": [
            {
                "request": {"prompt": "Hello", "use_context": False},
                "response": {"response": "👋 Hello! Welcome to Atlas AI!", "response_type": "conversational"},
            },
            {
                "request": {"prompt": "Tell me about Python"},
                "response": {"response": "Python is...", "response_type": "knowledge_based", "context_docs": 2},
            },
        ],
    },
    "feed-data": {
        "endpoint": "POST /api/feed-data",
        "description": "Add documents to the knowledge base",
        "request": {
            "content": "str - Document content",
            "title": "str - Document title",
        },
        "response": {
            "status": "str - 'success' or 'error'",
            "message": "str - Status message",
            "doc_id": "str - Document ID",
            "total_docs": "int - Total documents in KB",
        },
    },
    "knowledge-base": {
        "endpoint": "GET /api/knowledge-base",
        "description": "Get knowledge base statistics",
        "response": {
            "total_documents": "int - Number of documents",
            "status": "str - 'ready' or 'empty'",
        },
    },
}
