from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import chromadb
from chromadb.config import Settings
import os
from conversational import ConversationalAI
from knowledge.math.math_kb import MathKnowledgeBase

app = FastAPI()
math_kb = MathKnowledgeBase()

# Initialize conversational AI (offline, no Ollama needed)
conversation_engine = ConversationalAI()

# Allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize ChromaDB (local vector database)
data_dir = "./data"
os.makedirs(data_dir, exist_ok=True)
chroma_client = chromadb.PersistentClient(path=data_dir)
collection = chroma_client.get_or_create_collection(name="documents")

class ChatRequest(BaseModel):
    prompt: str
    model: str = "llama3"
    use_context: bool = True

class DocumentRequest(BaseModel):
    content: str
    title: str = "document"

@app.post("/api/feed-data")
async def feed_data(request: DocumentRequest):
    """Add documents to the local vector database"""
    try:
        # Get embedding from Ollama
        embedding_response = requests.post(
            "http://localhost:11434/api/embeddings",
            json={"model": "nomic-embed-text", "prompt": request.content}
        )
        embedding_response.raise_for_status()
        embedding = embedding_response.json().get("embedding", [])
        
        # Store in ChromaDB
        doc_id = f"doc_{collection.count() + 1}"
        collection.add(
            ids=[doc_id],
            embeddings=[embedding],
            documents=[request.content],
            metadatas=[{"title": request.title}]
        )
        
        return {
            "status": "success",
            "message": f"Document '{request.title}' added to knowledge base",
            "doc_id": doc_id,
            "total_docs": collection.count()
        }
    except Exception as e:
        return {"error": f"Failed to process document: {str(e)}"}

@app.post("/api/chat")
async def chat(request: ChatRequest):
    """Chat endpoint - checks conversational patterns first, then uses RAG/Ollama"""
    try:
        # First, check if this is a conversational message (greetings, small talk, etc.)
        conversational_response, is_conversational = conversation_engine.get_conversational_response(request.prompt)
        
        if is_conversational:
            # Return conversational response without using Ollama
            return {
                "response": conversational_response,
                "used_context": False,
                "context_docs": 0,
                "response_type": "conversational"
            }

        # Offline mathematics knowledge base (no Ollama required)
        math_results = math_kb.search(request.prompt, limit=3, min_score=2)
        if math_results:
            return {
                "response": math_kb.search_formatted(request.prompt, limit=3),
                "used_context": True,
                "context_docs": len(math_results),
                "response_type": "mathematics",
                "sources": [e["id"] for e in math_results],
            }
        
        # If not conversational, proceed with RAG + Ollama
        context = ""
        results = {"documents": [[]]}
        
        # If use_context is enabled and we have documents, retrieve relevant ones
        if request.use_context and collection.count() > 0:
            # Get embedding of the question
            embedding_response = requests.post(
                "http://localhost:11434/api/embeddings",
                json={"model": "nomic-embed-text", "prompt": request.prompt}
            )
            embedding_response.raise_for_status()
            query_embedding = embedding_response.json().get("embedding", [])
            
            # Query ChromaDB for relevant documents
            results = collection.query(
                query_embeddings=[query_embedding],
                n_results=3
            )
            
            if results["documents"] and results["documents"][0]:
                context = "\n\n".join(results["documents"][0])
                context = f"Context from knowledge base:\n{context}\n\n"
        
        # Prepare prompt with context
        full_prompt = f"{context}User question: {request.prompt}"
        
        # Call Ollama for response
        ollama_url = "http://localhost:11434/api/generate"
        payload = {
            "model": request.model,
            "prompt": full_prompt,
            "stream": False
        }
        
        response = requests.post(ollama_url, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        
        return {
            "response": data.get("response", "No response generated."),
            "used_context": request.use_context and collection.count() > 0,
            "context_docs": len(results["documents"][0]) if request.use_context and collection.count() > 0 else 0,
            "response_type": "knowledge_based"
        }
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to process request: {str(e)}"}

@app.get("/api/knowledge-base")
async def get_knowledge_base():
    """Get stats about the knowledge base"""
    return {
        "total_documents": collection.count(),
        "status": "ready" if collection.count() > 0 else "empty"
    }


@app.get("/api/math/stats")
async def math_stats():
    """Mathematics knowledge base statistics"""
    return {
        "total_entries": math_kb.count,
        "topics": math_kb.topics,
        "status": "ready",
    }


@app.get("/api/math/topics")
async def math_topics():
    """List available mathematics topics"""
    return {"topics": math_kb.topics}


@app.get("/api/math/search")
async def math_search(q: str, limit: int = 5):
    """Search mathematics knowledge by keyword"""
    results = math_kb.search(q, limit=min(limit, 20))
    return {
        "query": q,
        "count": len(results),
        "results": results,
    }


@app.get("/api/math/entry/{entry_id}")
async def math_entry(entry_id: str):
    """Get a single mathematics entry by ID"""
    entry = math_kb.get_by_id(entry_id)
    if not entry:
        return {"error": f"Entry '{entry_id}' not found"}
    return entry


@app.get("/api/math/topic/{topic}")
async def math_by_topic(topic: str):
    """List all entries for a topic (algebra, geometry, etc.)"""
    entries = math_kb.list_by_topic(topic)
    return {"topic": topic, "count": len(entries), "entries": entries}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
