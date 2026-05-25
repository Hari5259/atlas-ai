from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import chromadb
import os

from conversational import ConversationalAI
from knowledge.math.math_kb import MathKnowledgeBase
from knowledge.general_kb import general_kb
from knowledge_router import search_knowledge
from offline_responses import try_offline_response
from response_formatter import format_error, format_topics_list

app = FastAPI()
math_kb = MathKnowledgeBase()
conversation_engine = ConversationalAI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

data_dir = "./data"
os.makedirs(data_dir, exist_ok=True)
chroma_client = chromadb.PersistentClient(path=data_dir)
collection = chroma_client.get_or_create_collection(name="documents")

SYSTEM_PROMPT = (
    "You are Atlas, A Teach Learn and Study AI. Give clear, accurate, structured answers. "
    "Use markdown headings and bullet points. Be encouraging and educational. "
    "If unsure, say so. Keep responses focused and under 400 words unless asked for detail."
)


class ChatRequest(BaseModel):
    prompt: str
    model: str = "llama3"
    use_context: bool = True


class DocumentRequest(BaseModel):
    content: str
    title: str = "document"


def ollama_available() -> bool:
    try:
        r = requests.get("http://localhost:11434/api/tags", timeout=2)
        return r.status_code == 200
    except requests.RequestException:
        return False


@app.get("/api/health")
async def health():
    return {
        "status": "ok",
        "ollama": ollama_available(),
        "knowledge_entries": math_kb.count + general_kb.count,
        "uploaded_docs": collection.count(),
    }


@app.get("/api/knowledge/stats")
async def knowledge_stats():
    return {
        "mathematics": math_kb.count,
        "general": general_kb.count,
        "total": math_kb.count + general_kb.count,
        "topics": {
            "math": math_kb.topics,
            "general": general_kb.topics,
        },
    }


@app.post("/api/feed-data")
async def feed_data(request: DocumentRequest):
    try:
        embedding_response = requests.post(
            "http://localhost:11434/api/embeddings",
            json={"model": "nomic-embed-text", "prompt": request.content},
            timeout=60,
        )
        embedding_response.raise_for_status()
        embedding = embedding_response.json().get("embedding", [])
        doc_id = f"doc_{collection.count() + 1}"
        collection.add(
            ids=[doc_id],
            embeddings=[embedding],
            documents=[request.content],
            metadatas=[{"title": request.title}],
        )
        return {
            "status": "success",
            "message": f"Document '{request.title}' added to knowledge base",
            "doc_id": doc_id,
            "total_docs": collection.count(),
        }
    except Exception as e:
        return {"error": f"Failed to process document: {str(e)}"}


@app.post("/api/chat")
async def chat(request: ChatRequest):
    try:
        conversational_response, is_conversational = conversation_engine.get_conversational_response(
            request.prompt
        )
        if is_conversational:
            return {
                "response": conversational_response,
                "used_context": False,
                "context_docs": 0,
                "response_type": "conversational",
            }

        kb_text, kb_type, sources = search_knowledge(request.prompt, limit=3)
        if kb_text:
            return {
                "response": kb_text,
                "used_context": True,
                "context_docs": len(sources),
                "response_type": kb_type,
                "sources": sources,
            }

        offline = try_offline_response(request.prompt)
        if offline:
            return {
                "response": offline,
                "used_context": False,
                "context_docs": 0,
                "response_type": "offline",
            }

        context = ""
        results = {"documents": [[]]}
        if request.use_context and collection.count() > 0 and ollama_available():
            try:
                embedding_response = requests.post(
                    "http://localhost:11434/api/embeddings",
                    json={"model": "nomic-embed-text", "prompt": request.prompt},
                    timeout=30,
                )
                embedding_response.raise_for_status()
                query_embedding = embedding_response.json().get("embedding", [])
                results = collection.query(query_embeddings=[query_embedding], n_results=3)
                if results["documents"] and results["documents"][0]:
                    context = "Reference material:\n" + "\n\n".join(results["documents"][0]) + "\n\n"
            except requests.RequestException:
                pass

        if ollama_available():
            full_prompt = (
                f"{SYSTEM_PROMPT}\n\n{context}"
                f"User: {request.prompt}\n\nAssistant:"
            )
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={"model": request.model, "prompt": full_prompt, "stream": False},
                timeout=90,
            )
            response.raise_for_status()
            data = response.json()
            return {
                "response": data.get("response", "No response generated.").strip(),
                "used_context": bool(context),
                "context_docs": len(results["documents"][0]) if context else 0,
                "response_type": "knowledge_based",
            }

        all_topics = list(set(math_kb.topics + general_kb.topics))
        return {
            "response": format_topics_list(all_topics[:12]),
            "used_context": False,
            "context_docs": 0,
            "response_type": "fallback",
        }
    except requests.exceptions.RequestException as e:
        return {"error": format_error(str(e))}


@app.get("/api/knowledge-base")
async def get_knowledge_base():
    return {
        "total_documents": collection.count(),
        "status": "ready" if collection.count() > 0 else "empty",
    }


@app.get("/api/math/stats")
async def math_stats():
    return {"total_entries": math_kb.count, "topics": math_kb.topics, "status": "ready"}


@app.get("/api/math/search")
async def math_search(q: str, limit: int = 5):
    entries = math_kb.search_entries(q, limit=min(limit, 20))
    return {"query": q, "count": len(entries), "results": entries}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
