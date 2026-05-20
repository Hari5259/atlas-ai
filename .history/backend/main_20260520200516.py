from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

app = FastAPI()

# Allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    prompt: str
    model: str = "llama3" # Defaulting to the model we saw installed

@app.post("/api/chat")

async def chat(request: ChatRequest):
    # Call the local Ollama API
    ollama_url = "http://localhost:11434/api/generate"
    payload = {
        "model": request.model,
        "prompt": request.prompt,
        "stream": False
    }
    
    try:
        response = requests.post(ollama_url, json=payload)
        response.raise_for_status()
        data = response.json()
        return {"response": data.get("response", "No response generated.")}
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to connect to Ollama. Make sure Ollama is running! Error: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
