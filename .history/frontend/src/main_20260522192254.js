import './style.css'

const API_URL = 'http://localhost:8000'

// Initialize app
document.querySelector('#app').innerHTML = `
  <div class="container">
    <header>
      <h1>🤖 Atlas AI</h1>
      <p>Local AI with Your Own Data</p>
    </header>
    
    <div class="main-content">
      <!-- Sidebar: Data Feed -->
      <aside class="sidebar">
        <h2>📚 Knowledge Base</h2>
        <div id="kb-stats" class="kb-stats">
          <p>Documents: <span id="doc-count">0</span></p>
          <p>Status: <span id="kb-status">Loading...</span></p>
        </div>
        
        <div class="feed-section">
          <h3>Feed Data</h3>
          <textarea id="data-input" placeholder="Paste your data here (documents, facts, knowledge, etc.)" rows="6"></textarea>
          <input type="text" id="data-title" placeholder="Document title" value="Document">
          <button id="feed-btn" class="btn btn-primary">Add to Knowledge Base</button>
          <div id="feed-status" class="status-message"></div>
        </div>
      </aside>
      
      <!-- Main: Chat -->
      <main class="chat-section">
        <div id="chat-messages" class="chat-messages">
          <div class="message bot-message">
            <p>Hello! 👋 I'm Atlas AI. Feed me your data and ask me questions about it!</p>
          </div>
        </div>
        
        <div class="chat-input-area">
          <div class="input-group">
            <input type="text" id="chat-input" placeholder="Ask me anything..." autocomplete="off">
            <button id="send-btn" class="btn btn-primary">Send</button>
          </div>
          <label class="checkbox">
            <input type="checkbox" id="use-context" checked>
            Use Knowledge Base
          </label>
        </div>
      </main>
    </div>
  </div>
`

// State
let messages = []

// Elements
const dataInput = document.querySelector('#data-input')
const dataTitle = document.querySelector('#data-title')
const feedBtn = document.querySelector('#feed-btn')
const feedStatus = document.querySelector('#feed-status')
const chatInput = document.querySelector('#chat-input')
const sendBtn = document.querySelector('#send-btn')
const chatMessages = document.querySelector('#chat-messages')
const useContextCheckbox = document.querySelector('#use-context')

// Load knowledge base stats
async function loadKnowledgeBase() {
  try {
    const res = await fetch(`${API_URL}/api/knowledge-base`)
    const data = await res.json()
    document.querySelector('#doc-count').textContent = data.total_documents
    document.querySelector('#kb-status').textContent = data.status === 'ready' ? '✅ Ready' : '⚠️ Empty'
  } catch (error) {
    console.error('Failed to load KB:', error)
  }
}

// Feed data
feedBtn.addEventListener('click', async () => {
  const content = dataInput.value.trim()
  const title = dataTitle.value || 'Document'
  
  if (!content) {
    showStatus('Please enter some data', 'error')
    return
  }
  
  feedBtn.disabled = true
  showStatus('Adding data...', 'info')
  
  try {
    const res = await fetch(`${API_URL}/api/feed-data`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ content, title })
    })
    
    const result = await res.json()
    
    if (result.error) {
      showStatus(`Error: ${result.error}`, 'error')
    } else {
      showStatus(`✅ ${result.message}`, 'success')
      dataInput.value = ''
      dataTitle.value = 'Document'
      loadKnowledgeBase()
    }
  } catch (error) {
    showStatus(`Error: ${error.message}`, 'error')
  } finally {
    feedBtn.disabled = false
  }
})

// Send message
async function sendMessage() {
  const message = chatInput.value.trim()
  if (!message) return
  
  chatInput.value = ''
  
  // Add user message
  addMessage('user', message)
  sendBtn.disabled = true
  
  try {
    const res = await fetch(`${API_URL}/api/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        prompt: message,
        model: 'llama3',
        use_context: useContextCheckbox.checked
      })
    })
    
    const result = await res.json()
    
    if (result.error) {
      addMessage('bot', `❌ Error: ${result.error}`)
    } else {
      let botMsg = result.response
      
      // Add response type indicator
      if (result.response_type === 'conversational') {
        botMsg += '\n\n_💬 Quick response_'
      } else if (result.used_context) {
        botMsg += `\n\n_📚 Based on ${result.context_docs} document(s)_`
      } else if (result.response_type === 'knowledge_based') {
        botMsg += `\n\n_🧠 AI generated response_`
      }
      
      addMessage('bot', botMsg)
    }
  } catch (error) {
    addMessage('bot', `❌ Connection error: ${error.message}`)
  } finally {
    sendBtn.disabled = false
    chatInput.focus()
  }
}

sendBtn.addEventListener('click', sendMessage)
chatInput.addEventListener('keypress', (e) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault()
    sendMessage()
  }
})

// Helper functions
function addMessage(role, content) {
  const msgDiv = document.createElement('div')
  msgDiv.className = `message ${role}-message`
  msgDiv.innerHTML = `<p>${content}</p>`
  chatMessages.appendChild(msgDiv)
  chatMessages.scrollTop = chatMessages.scrollHeight
}

function showStatus(message, type) {
  feedStatus.textContent = message
  feedStatus.className = `status-message ${type}`
  setTimeout(() => {
    feedStatus.textContent = ''
    feedStatus.className = 'status-message'
  }, 5000)
}

// Initialize
loadKnowledgeBase()
setInterval(loadKnowledgeBase, 10000) // Refresh KB stats every 10 seconds
