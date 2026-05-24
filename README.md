# Atlas

**A Teach, Learn and Study AI** — a locally running offline learning assistant built with custom-trained responses and local LLM integration. Atlas focuses on private study sessions, clear explanations, and intelligent help without relying on cloud APIs.

---

## Features

* Beautiful landing page with **Get Started** (no login required)
* **A · Teach · L · Learn · S · Study · AI** branding
* Offline AI assistant
* Local AI inference using Ollama
* Custom-trained response system
* Semantic response handling
* Interactive user interface
* Fast local processing
* Private and secure AI interaction
* Expandable training dataset
* **Mathematics knowledge base** — 30+ offline math entries (algebra, geometry, calculus, trigonometry, statistics, linear algebra)

---

## Tech Stack

### Frontend

* HTML
* CSS
* JavaScript

### AI / Backend

* Python
* Ollama
* Local LLM Integration
* Custom Response Training

---

## Project Goal

The goal of Atlas AI is to create a fully local AI assistant capable of understanding and responding intelligently using locally trained data and offline AI models.

Unlike cloud-based assistants, Atlas AI focuses on:

* Privacy
* Local execution
* Faster response handling
* Custom AI behavior
* Offline accessibility

---

## Folder Structure

```bash
atlas-ai/
│
├── public/
├── src/
├── index.html
├── package.json
├── package-lock.json
└── README.md
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/Hari5259/atlas-ai.git
```

### Open Project

```bash
cd atlas-ai
```

### Install Dependencies

```bash
npm install
```

---

## Run Ollama

Install Ollama:

[https://ollama.com/](https://ollama.com/)

Run a local model:

```bash
ollama run llama3
```

---

## Run Project

```bash
cd frontend
npm install
npm run dev
```

Open the URL shown in the terminal. You will see the **Atlas** landing page — click **Get Started** to open the study chat (no account required).

### Mathematics Knowledge Base

The backend includes structured math data under `backend/knowledge/math/`. Search works offline without Ollama:

```bash
cd backend
python -m uvicorn main:app --reload
# GET http://localhost:8000/api/math/search?q=quadratic+formula
# GET http://localhost:8000/api/math/stats
```

Optional: seed math into ChromaDB for vector search (requires Ollama):

```bash
cd backend
python knowledge/math/seed_math_kb.py
```

---

## Future Improvements

* Voice assistant integration
* Memory system
* PDF and document interaction
* Advanced semantic retrieval
* Personalized AI behavior
* AI note summarization
* Real-time local training

---

## Author

Hari

---

## License

This project is developed for educational and learning purposes.
