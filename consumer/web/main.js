// Altere a URL abaixo para a do API Gateway WebSocket "apw-app" após o deploy
const WS_URL = 'wss://nkmudo1tmg.execute-api.us-east-1.amazonaws.com/prod/';

const chatWindow = document.getElementById('chat-window');
const promptForm = document.getElementById('prompt-form');
const promptInput = document.getElementById('prompt-input');

let ws;

function appendMessage(text, sender, id = null) {
  let msgDiv;
  if (id) {
    msgDiv = document.getElementById(id);
    if (!msgDiv) {
      msgDiv = document.createElement('div');
      msgDiv.className = `message ${sender}`;
      msgDiv.id = id;
      chatWindow.appendChild(msgDiv);
    }
    msgDiv.textContent += (msgDiv.textContent ? ' ' : '') + text;
  } else {
    msgDiv = document.createElement('div');
    msgDiv.className = `message ${sender}`;
    msgDiv.textContent = text;
    chatWindow.appendChild(msgDiv);
  }
  
  requestAnimationFrame(() => {
    chatWindow.scrollTop = chatWindow.scrollHeight;

    if (chatWindow.lastElementChild) {
      chatWindow.lastElementChild.scrollIntoView({ behavior: 'auto', block: 'end' });
    }

    requestAnimationFrame(() => {
      chatWindow.scrollTop = chatWindow.scrollHeight;
    });
  });
}

function connectWS() {
  ws = new WebSocket(WS_URL);

  ws.onopen = () => {
    appendMessage('Conectado ao servidor!', 'bot');
  };

  let streamingId = null;
  ws.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data);
      if (data.type === 'stream') {
        if (!streamingId) streamingId = 'stream-' + Date.now();
        appendMessage(data.chunk, 'bot', streamingId);
      } else if (data.type === 'end') {
        streamingId = null;
      } else if (data.message) {
        appendMessage(data.message, 'bot');
      }
    } catch {
      appendMessage(event.data, 'bot');
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
  appendMessage(prompt, 'user');
  ws.send(JSON.stringify({ action: 'sendPrompt', prompt }));
  promptInput.value = '';
});

connectWS();
