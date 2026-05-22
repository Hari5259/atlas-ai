# Atlas AI - Local AI with Your Own Data

A full-stack application that combines local LLMs with a vector database for intelligent Q&A over your own data.

## Architecture

- **Backend**: FastAPI server with ChromaDB vector database
- **Frontend**: Vite + JavaScript with real-time chat interface
- **LLM**: Ollama (local language model)
- **Vector Store**: ChromaDB (local vector database)

## Prerequisites

1. **Ollama** installed and running
   - Download from https://ollama.ai
   - Required models:
     - `llama3` (for chat)
     - `nomic-embed-text` (for embeddings)
   
   Pull models with:
   ```bash
   ollama pull llama3
   ollama pull nomic-embed-text
   ```

2. **Python 3.8+** for backend
3. **Node.js 16+** for frontend

## Setup & Running

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
python main.py
```

The backend will start at `http://localhost:8000`

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The frontend will start at `http://localhost:5173` (or shown in terminal)

## How to Use

### 1. Feed Your Data

In the left sidebar:
- Paste your documents, text, or knowledge in the textarea
- Give it a title
- Click "Add to Knowledge Base"
- The data is embedded and stored locally in ChromaDB

### 2. Ask Questions

In the chat area:
- Type your question
- Make sure "Use Knowledge Base" is checked
- Hit Enter or click Send
- The AI will search your data and generate relevant answers

### 3. Knowledge Base Stats

The sidebar shows:
- Total documents uploaded
- Status (Ready/Empty)
- Auto-refreshes every 10 seconds

## API Endpoints

### `/api/feed-data` (POST)
Add documents to the vector database
```json
{
  "content": "Your document text here",
  "title": "Document Title"
}
```

### `/api/chat` (POST)
Chat with optional context from knowledge base
```json
{
  "prompt": "Your question",
  "model": "llama3",
  "use_context": true
}
```

### `/api/knowledge-base` (GET)
Get knowledge base statistics

## Data Storage

- Documents are stored in `./data` directory (inside backend folder)
- Uses ChromaDB's persistent client
- Data persists between sessions

## Troubleshooting

**"Failed to connect to Ollama"**
- Make sure Ollama is running: `ollama serve`
- Check that http://localhost:11434 is accessible

**"Model not found"**
- Pull the required models:
  ```bash
  ollama pull llama3
  ollama pull nomic-embed-text
  ```

**"CORS errors"**
- Backend already has CORS enabled for all origins
- Make sure frontend is connecting to correct backend URL

**Empty knowledge base**
- Feed some data first using the sidebar textarea
- Check the knowledge base stats

## Features

✅ Local LLM inference (Ollama)
✅ Vector embeddings with ChromaDB
✅ Semantic search over your data
✅ Real-time chat interface
✅ Knowledge base statistics
✅ Toggle context usage on/off
✅ Fully offline (no external APIs)
✅ Fast and responsive UI

## Example Workflows

### Research Assistant
1. Feed research papers or articles
2. Ask questions about the content
3. Get AI-generated summaries and insights

### Documentation Bot
1. Add company/project documentation
2. Users can query documentation naturally
3. Faster than manual search

### Learning Tool
1. Feed textbooks or course materials
2. Ask questions to test understanding
3. Get explanations based on materials

## Performance Tips

- Start with smaller documents for faster processing
- Use clear, structured data for better embeddings
- Ask specific questions for better answers
- Monitor system resources when running large models

## Future Enhancements

- Multi-file upload support
- Document management UI
- Conversation history
- Different embedding models
- Batch processing
- Export/Import knowledge bases

---

Built with ❤️ for local AI enthusiasts
