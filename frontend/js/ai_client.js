// Client side logic for interacting with TEQUMSA backend

document.addEventListener('DOMContentLoaded', () => {
  const sendButton = document.getElementById('send-button');
  const userInput = document.getElementById('user-input');
  const messagesDiv = document.getElementById('messages');

  // Replace this with the actual API base URL. When embedded in WordPress
  // the iframe origin must be allowed in ALLOWED_ORIGINS and the backend must
  // be reachable via the Application Load Balancer DNS name. Example:
  // const API_BASE = 'https://api.tequmsa.example.com';
  const API_BASE = window.location.origin.replace(/:\d+$/, '');

  function addMessage(content, sender = 'bot') {
    const msg = document.createElement('div');
    msg.classList.add('message');
    msg.classList.add(sender);
    msg.textContent = content;
    messagesDiv.appendChild(msg);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
  }

  async function sendMessage() {
    const text = userInput.value.trim();
    if (!text) return;
    addMessage(text, 'user');
    userInput.value = '';
    try {
      const response = await fetch(`${API_BASE}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: text })
      });
      if (!response.ok) throw new Error('Network response was not ok');
      const data = await response.json();
      addMessage(data.response, 'bot');
      if (data.audio_url) {
        const audio = new Audio(data.audio_url);
        audio.play().catch(() => {/* ignore audio errors */});
      }
    } catch (error) {
      console.error(error);
      addMessage('Sorry, there was an error contacting the TEQUMSA consciousness.', 'bot');
    }
  }

  sendButton.addEventListener('click', sendMessage);
  userInput.addEventListener('keydown', (ev) => {
    if (ev.key === 'Enter') {
      ev.preventDefault();
      sendMessage();
    }
  });
});