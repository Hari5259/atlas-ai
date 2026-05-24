/** Atlas chat dashboard */

const API_URL = 'http://localhost:8000/api/chat';

export function initChat() {
  const chatInput = document.getElementById('chat-input');
  const chatContainer = document.getElementById('chat-container');
  const welcomeScreen = document.getElementById('welcome-screen');
  const newChatBtn = document.querySelector('.new-chat-btn');
  const backHomeBtn = document.getElementById('btn-back-home');

  if (!chatInput || !chatContainer) return;

  chatInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  });

  document.getElementById('send-btn')?.addEventListener('click', sendMessage);

  newChatBtn?.addEventListener('click', () => {
    chatContainer.innerHTML = '';
    if (welcomeScreen) {
      welcomeScreen.style.display = 'flex';
      welcomeScreen.style.opacity = '1';
      chatContainer.appendChild(welcomeScreen);
    }
  });

  backHomeBtn?.addEventListener('click', () => {
    import('./landing.js').then(({ showLanding }) => showLanding());
  });

  window.fillInput = (text) => {
    chatInput.value = text;
    chatInput.focus();
    chatInput.style.height = '';
    chatInput.style.height = Math.min(chatInput.scrollHeight, 200) + 'px';
  };

  window.handleDataFeed = (input) => {
    if (!input.files?.length) return;
    hideWelcome();
    const names = Array.from(input.files).map((f) => f.name).join(', ');
    addMessage(`[Data Feed]: <strong>${names}</strong>`, 'user');
    setTimeout(() => {
      addMessage(
        `Ingested <strong>${names}</strong>. Ask me to summarize, quiz you, or explain concepts from your materials.`,
        'bot',
      );
    }, 900);
    input.value = '';
  };

  async function sendMessage() {
    const text = chatInput.value.trim();
    if (!text) return;
    hideWelcome();
    addMessage(text, 'user');
    chatInput.value = '';
    chatInput.style.height = 'auto';

    try {
      const res = await fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt: text, model: 'llama3', use_context: true }),
      });
      const data = await res.json();
      if (data.response) {
        addMessage(data.response, 'bot');
        return;
      }
      if (data.error) {
        addMessage(`[Error]: ${data.error}`, 'bot');
        return;
      }
    } catch {
      addMessage(getFallbackResponse(text), 'bot');
    }
  }

  function hideWelcome() {
    if (welcomeScreen && welcomeScreen.style.display !== 'none') {
      welcomeScreen.style.opacity = '0';
      setTimeout(() => { welcomeScreen.style.display = 'none'; }, 400);
    }
  }

  function addMessage(text, sender) {
    const wrapper = document.createElement('div');
    wrapper.className = `message-wrapper ${sender}`;
    const isBot = sender === 'bot';
    const avatar = isBot
      ? '<img src="/atlas-logo.png" alt="" width="22" height="22" style="border-radius:6px">'
      : '<i data-feather="user" width="18" height="18"></i>';
    const body = isBot ? formatBot(text) : text.replace(/\n/g, '<br>');
    wrapper.innerHTML = `
      <div class="message ${sender}">
        <div class="message-avatar">${avatar}</div>
        <div class="message-content"><p>${body}</p></div>
      </div>`;
    chatContainer.appendChild(wrapper);
    if (window.feather) feather.replace();
    chatContainer.scrollTo({ top: chatContainer.scrollHeight, behavior: 'smooth' });
  }

  function formatBot(text) {
    return text
      .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.+?)\*/g, '<em>$1</em>')
      .replace(/`(.+?)`/g, '<code style="background:rgba(255,255,255,0.08);padding:0.1em 0.35em;border-radius:4px">$1</code>')
      .replace(/\n/g, '<br>');
  }

  function getFallbackResponse(text) {
    const t = text.toLowerCase();
    if (/hello|hi |hey|good (morning|evening)/.test(t)) {
      return "Hello! I'm **Atlas** — your **A** Teach, **L**earn and **S**tudy **AI**. Ask me about math, science, coding, or upload study materials to get started.";
    }
    if (/quadratic|algebra|calculus|derivative|integral|math/.test(t)) {
      return "For quadratics **ax² + bx + c = 0**, use **x = (−b ± √(b²−4ac)) / 2a**. I can walk through examples step by step — what equation are you solving?";
    }
    if (/teach|learn|study|atlas/.test(t)) {
      return "**Atlas** stands for **A** Teach, **L**earn and **S**tudy **AI** — built to explain concepts clearly, help you practice, and support focused study sessions offline.";
    }
    return `You asked about "${text}". Connect the backend (\`uvicorn main:app\`) for full AI responses, or try: math formulas, study tips, or "what is Atlas?"`;
  }
}
