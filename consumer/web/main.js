// Altere a URL abaixo para a do API Gateway WebSocket "apw-app" após o deploy
const WS_URL = 'wss://nkmudo1tmg.execute-api.us-east-1.amazonaws.com/prod/';

const chatWindow = document.getElementById('chat-window');
const promptForm = document.getElementById('prompt-form');
const promptInput = document.getElementById('prompt-input');

let ws;
let currentBotMessage = null;

function appendMessage(text, sender, isStreaming = false) {
  // If it's a bot message and we're streaming, append to the current message
  if (sender === 'bot' && isStreaming) {
    if (!currentBotMessage) {
      currentBotMessage = document.createElement('div');
      currentBotMessage.className = 'message bot';
      chatWindow.appendChild(currentBotMessage);
    }
    currentBotMessage.textContent += text;
  } else {
    // For new messages or user messages, create a new message element
    if (currentBotMessage) {
      currentBotMessage = null;
    }
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${sender}`;
    msgDiv.textContent = text;
    chatWindow.appendChild(msgDiv);
  }
  
  // Auto-scroll to the new message
  chatWindow.scrollTop = chatWindow.scrollHeight;
}

function connectWS() {
  ws = new WebSocket(WS_URL);

  ws.onopen = () => {
    appendMessage('Conectado ao servidor!', 'bot');
  };

  ws.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data);
      if (data.type === 'stream') {
        appendMessage(data.chunk, 'bot', true);
      } else if (data.type === 'end') {
        currentBotMessage = null;
      } else if (data.message) {
        appendMessage(data.message, 'bot', false);
      }
    } catch (e) {
      console.error('Error processing message:', e);
      appendMessage('Error processing message', 'bot');
    }
  };

  ws.onclose = () => {
    appendMessage('Desconectado. Tentando reconectar...', 'bot');
    setTimeout(connectWS, 2000);
  };

  ws.onerror = (err) => {
    appendMessage('Erro de conexão!', 'bot');
  };
}

promptForm.addEventListener('submit', (e) => {
  e.preventDefault();
  const prompt = promptInput.value.trim();
  if (!prompt || ws.readyState !== WebSocket.OPEN) return;
  
  // Show user message
  appendMessage(prompt, 'user');
  
  // Send to WebSocket
  ws.send(JSON.stringify({ action: 'sendPrompt', prompt }));
  promptInput.value = '';
  promptInput.focus();
});

connectWS();
