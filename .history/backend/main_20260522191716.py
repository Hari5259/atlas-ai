from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import chromadb
from chromadb.config import Settings
import os

app = FastAPI()

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
    """Chat with RAG - retrieves context from local data if available"""
    try:
        context = ""
        
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
            "context_docs": len(results["documents"][0]) if request.use_context and collection.count() > 0 else 0
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
