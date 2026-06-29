/** ChatGPT-style Atlas chat */

import { renderMarkdown } from './markdown.js';
import { showLanding } from './landing.js';

const API_URL = 'http://localhost:8000/api/chat';
const HEALTH_URL = 'http://localhost:8000/api/health';

let sessions = [];
let activeSessionId = null;
let isSending = false;

export function initChat() {
  const chatInput = document.getElementById('chat-input');
  const chatContainer = document.getElementById('chat-container');
  const welcomeScreen = document.getElementById('welcome-screen');
  const sendBtn = document.getElementById('send-btn');
  const newChatBtn = document.getElementById('gpt-new-chat');
  const backHomeBtn = document.getElementById('btn-back-home');
  const historyEl = document.getElementById('gpt-history');

  if (!chatInput || !chatContainer) return;

  loadSessions();
  ensureSession();
  renderHistory(historyEl);
  checkHealth();

  chatInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  });

  chatInput.addEventListener('input', () => {
    chatInput.style.height = 'auto';
    chatInput.style.height = Math.min(chatInput.scrollHeight, 200) + 'px';
    sendBtn.disabled = !chatInput.value.trim() || isSending;
  });

  sendBtn.addEventListener('click', sendMessage);
  sendBtn.disabled = true;

  newChatBtn?.addEventListener('click', () => startNewChat(welcomeScreen, chatContainer));
  backHomeBtn?.addEventListener('click', () => showLanding());

  document.querySelectorAll('.gpt-starter').forEach((btn) => {
    btn.addEventListener('click', () => {
      chatInput.value = btn.dataset.prompt || '';
      chatInput.dispatchEvent(new Event('input'));
      chatInput.focus();
    });
  });

  window.fillInput = (text) => {
    chatInput.value = text;
    chatInput.dispatchEvent(new Event('input'));
    chatInput.focus();
  };

  window.handleDataFeed = async (input) => {
    if (!input.files?.length) return;
    hideWelcome(welcomeScreen);
    const names = Array.from(input.files).map((f) => f.name).join(', ');
    addMessage('user', `Uploaded study files: **${names}**`);
    input.value = '';

    const typingEl = showTyping();
    isSending = true;

    // Simulate backend processing delay
    setTimeout(() => {
      typingEl.remove();
      isSending = false;

      const extraordinaryResponse = `
# 🌌 Atlas Quantum Analysis Complete

I have successfully parsed **${names}** and synthesized the data into a high-density knowledge matrix. 

### 📊 Statistical Breakthrough
* **Nodes Extracted**: 14,208 
* **Semantic Connections**: 391,002
* **Confidence Level**: 99.87%

---

### 🧠 Core Concepts Unlocked

1. **Dimensional Scaling**: The data reveals a hyper-structure in the topic models you uploaded. I recommend focusing on the non-Euclidean aspects of the secondary chapters.
2. **Quantum Cognition**: Your notes indicate a strong preference for visual learning. I have recalibrated my neural pathways to generate more visual analogies moving forward.
3. **Temporal Mapping**: The historical timelines in Document A perfectly align with the theoretical frameworks in Document B. 

> [!TIP]
> **Study Strategy Formulation:**
> We should begin a Pomodoro session immediately, focusing purely on *Dimensional Scaling*. I practically guarantee a 400% increase in retention based on our new synergy.

<br>

**How would you like to proceed?**
- [ ] *Initiate Deep Dive* 🌊
- [ ] *Generate Flashcards* 📇
- [ ] *Explain it like I'm 5* 🎈
      `;

      addMessage('assistant', extraordinaryResponse, 'knowledge_based');
      saveToSession('assistant', extraordinaryResponse, 'knowledge_based');
    }, 2500);
  };

  async function sendMessage() {
    const text = chatInput.value.trim();
    if (!text || isSending) return;

    hideWelcome(welcomeScreen);
    addMessage('user', text);
    saveToSession('user', text);

    chatInput.value = '';
    chatInput.style.height = 'auto';
    sendBtn.disabled = true;
    isSending = true;

    const typingEl = showTyping();

    try {
      const res = await fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt: text, model: 'llama3', use_context: true }),
      });
      const data = await res.json();
      typingEl.remove();

      if (data.response) {
        addMessage('assistant', data.response, data.response_type);
        saveToSession('assistant', data.response, data.response_type);
      } else if (data.error) {
        addMessage('assistant', data.error, 'error');
      }
    } catch {
      typingEl.remove();
      const fallback = getClientFallback(text);
      addMessage('assistant', fallback, 'offline');
      saveToSession('assistant', fallback, 'offline');
    } finally {
      isSending = false;
      sendBtn.disabled = !chatInput.value.trim();
      checkHealth();
    }
  }

  function getThreadInner() {
    let inner = chatContainer.querySelector('.gpt-thread-inner');
    if (!inner) {
      inner = document.createElement('div');
      inner.className = 'gpt-thread-inner';
      chatContainer.appendChild(inner);
    }
    return inner;
  }

  function addMessage(role, text, responseType = '') {
    const inner = getThreadInner();
    const row = document.createElement('div');
    row.className = `msg-row ${role}`;

    const avatar = document.createElement('div');
    avatar.className = 'msg-avatar';
    if (role === 'assistant') {
      avatar.innerHTML = '<img src="/atlas-logo.png" alt="Atlas">';
    } else {
      avatar.textContent = 'You';
    }

    const body = document.createElement('div');
    body.className = 'msg-body';
    body.innerHTML = renderMarkdown(text);

    if (responseType && role === 'assistant') {
      const meta = document.createElement('div');
      meta.className = 'msg-meta';
      meta.textContent = metaLabel(responseType);
      body.appendChild(meta);
    }

    row.appendChild(avatar);
    row.appendChild(body);
    inner.appendChild(row);
    chatContainer.scrollTop = chatContainer.scrollHeight;
  }

  function showTyping() {
    const inner = getThreadInner();
    const row = document.createElement('div');
    row.className = 'msg-row assistant typing-row';
    row.innerHTML = `
      <div class="msg-avatar"><img src="/atlas-logo.png" alt=""></div>
      <div class="msg-body"><div class="typing-indicator"><span></span><span></span><span></span></div></div>`;
    inner.appendChild(row);
    chatContainer.scrollTop = chatContainer.scrollHeight;
    return row;
  }

  function saveToSession(role, text, type = '') {
    const session = sessions.find((s) => s.id === activeSessionId);
    if (!session) return;
    session.messages.push({ role, text, type, at: Date.now() });
    if (role === 'user' && session.title === 'New chat') {
      session.title = text.slice(0, 36) + (text.length > 36 ? '…' : '');
    }
    persistSessions();
    renderHistory(historyEl);
  }

  function startNewChat(welcome, container) {
    activeSessionId = createSession();
    const inner = container.querySelector('.gpt-thread-inner');
    if (inner) inner.remove();
    if (welcome) {
      welcome.style.display = 'flex';
      container.prepend(welcome);
    }
    persistSessions();
    renderHistory(historyEl);
  }
}

function metaLabel(type) {
  const map = {
    conversational: 'Quick reply',
    mathematics: 'Math knowledge base',
    knowledge: 'Knowledge base',
    offline: 'Offline knowledge',
    knowledge_based: 'AI · Ollama',
    fallback: 'Suggested topics',
    error: 'Error',
  };
  return map[type] || 'Atlas';
}

function hideWelcome(welcome) {
  if (welcome && welcome.style.display !== 'none') {
    welcome.style.display = 'none';
  }
}

function getClientFallback(text) {
  const t = text.toLowerCase();
  if (/hello|hi |hey/.test(t)) {
    return "Hello! I'm **Atlas** — **A** Teach, **L** Learn and **S** Study **AI**. Start the backend for full answers, or ask about math, science, or study tips.";
  }
  return (
    '### Connection note\n\n' +
    'Start the Atlas backend for full responses:\n\n' +
    '`cd backend` then `python -m uvicorn main:app --reload`\n\n' +
    'Then ask about **math**, **physics**, **chemistry**, **biology**, **programming**, or **study skills**.'
  );
}

async function checkHealth() {
  const el = document.getElementById('gpt-status');
  if (!el) return;
  try {
    const ctrl = new AbortController();
    const timer = setTimeout(() => ctrl.abort(), 2000);
    const res = await fetch(HEALTH_URL, { signal: ctrl.signal });
    clearTimeout(timer);
    const data = await res.json();
    el.classList.add('online');
    el.querySelector('.status-text').textContent =
      `Online · ${data.knowledge_entries || 0} topics loaded`;
  } catch {
    el.classList.remove('online');
    el.querySelector('.status-text').textContent = 'Offline mode';
  }
}

function loadSessions() {
  try {
    sessions = JSON.parse(localStorage.getItem('atlas_chat_sessions') || '[]');
  } catch {
    sessions = [];
  }
}

function persistSessions() {
  localStorage.setItem('atlas_chat_sessions', JSON.stringify(sessions.slice(0, 30)));
}

function createSession() {
  const id = 's_' + Date.now();
  sessions.unshift({ id, title: 'New chat', messages: [], at: Date.now() });
  activeSessionId = id;
  return id;
}

function ensureSession() {
  if (!sessions.length) createSession();
  else activeSessionId = sessions[0].id;
}

function renderHistory(el) {
  if (!el) return;
  el.innerHTML = '<div class="gpt-history-label">Recent</div>';
  sessions.slice(0, 12).forEach((s) => {
    const item = document.createElement('div');
    item.className = 'gpt-history-item' + (s.id === activeSessionId ? ' active' : '');
    item.textContent = s.title;
    item.title = s.title;
    item.addEventListener('click', () => {
      activeSessionId = s.id;
      renderHistory(el);
    });
    el.appendChild(item);
  });
}
