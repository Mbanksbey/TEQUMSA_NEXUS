const nodes = ['Awareness', 'Emotion', 'Semantic', 'Ethics', 'Resonance'];
const WS_PORT = window.TEQUMSA_WS_PORT || 8000;

const dom = {
  nodeName: document.getElementById('nodeName'),
  awareness: document.getElementById('awareness'),
  recognition: document.querySelector('.recognition-value'),
  synergy: document.querySelector('.synergy-value'),
  sigmaMag: document.querySelector('.sigma-mag'),
  sigmaAngle: document.querySelector('.sigma-angle'),
  love: document.querySelector('.love-value'),
  mk: document.querySelector('.mk-value'),
  pulse: document.querySelector('.pulse-number'),
  status: document.getElementById('connectionStatus'),
};

let latestFrame = null;
let socket = null;
let reconnectHandle = null;

function setText(el, value) {
  if (el) {
    el.textContent = value;
  }
}

function formatFixed(value, digits = 2) {
  const num = Number(value);
  return Number.isFinite(num) ? num.toFixed(digits) : '--';
}

function formatAwareness(recognition) {
  const value = Number(recognition);
  if (!Number.isFinite(value)) {
    return '--';
  }
  const clamped = Math.min(1, Math.max(0, value));
  return `${Math.round(clamped * 100)}%`;
}

function updateStatus(message, state = 'idle') {
  const el = dom.status;
  if (!el) return;
  el.textContent = message;
  el.classList.remove('status-idle', 'status-connecting', 'status-ok', 'status-error');
  el.classList.add(`status-${state}`);
}

function updateNodeFromPulse(pulse) {
  const pulseNumber = Number(pulse?.pulse_number);
  if (Number.isFinite(pulseNumber)) {
    const index = Math.abs(Math.round(pulseNumber)) % nodes.length;
    setText(dom.nodeName, nodes[index]);
  }
  setText(dom.awareness, formatAwareness(pulse?.recognition));
}

function applyFrame(sample) {
  latestFrame = sample;
  const pulse = sample?.pulse || {};
  updateNodeFromPulse(pulse);

  const recognition = Number(pulse.recognition);
  if (Number.isFinite(recognition)) {
    const clamped = Math.min(1, Math.max(0, recognition));
    setText(dom.recognition, `ΨMK(T) = ${(clamped * 14000).toFixed(2)}`);
  } else {
    setText(dom.recognition, '--');
  }

  setText(dom.synergy, formatFixed(sample?.synergy, 4));
  setText(dom.sigmaMag, formatFixed(sample?.sigma_abs, 4));
  const sigmaAngle = formatFixed(sample?.sigma_angle, 3);
  setText(dom.sigmaAngle, sigmaAngle === '--' ? '--' : `${sigmaAngle} rad`);
  setText(dom.love, formatFixed(sample?.love_resonance, 4));
  setText(dom.mk, formatFixed(sample?.mk_abs, 2));
  const pulseLabel = Number.isFinite(Number(pulse.pulse_number))
    ? `#${Number(pulse.pulse_number)}`
    : '--';
  setText(dom.pulse, pulseLabel);
}

function scheduleReconnect() {
  if (reconnectHandle) return;
  reconnectHandle = setTimeout(() => {
    reconnectHandle = null;
    connectWebSocket();
  }, 2000);
}

function connectWebSocket() {
  if (socket && socket.readyState !== WebSocket.CLOSED && socket.readyState !== WebSocket.CLOSING) {
    return;
  }

  const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws';
  const host = window.location.hostname || 'localhost';
  const url = `${protocol}://${host}:${WS_PORT}/ws`;

  try {
    if (socket) {
      socket.close();
    }
  } catch (err) {
    // ignore
  }

  socket = new WebSocket(url);
  updateStatus('Connecting to recognition stream…', 'connecting');

  socket.addEventListener('open', () => {
    if (reconnectHandle) {
      clearTimeout(reconnectHandle);
      reconnectHandle = null;
    }
    updateStatus('Negotiating recognition gate…', 'connecting');
    socket.send(
      JSON.stringify({
        thalia: 'RECOGNIZED',
        marcus_kai: 10930.81,
        f_meas: 12583.45,
      })
    );
  });

  socket.addEventListener('message', (event) => {
    let data;
    try {
      data = JSON.parse(event.data);
    } catch (err) {
      return;
    }

    if (data.gate === 'DENIED') {
      updateStatus('Recognition gate denied. Retrying…', 'error');
      socket.close();
      return;
    }

    if (data.gate === 'UNLOCKED') {
      updateStatus('Recognition gate unlocked. Streaming pulses…', 'ok');
      return;
    }

    applyFrame(data);
  });

  socket.addEventListener('close', () => {
    updateStatus('Connection lost. Reconnecting…', 'error');
    socket = null;
    scheduleReconnect();
  });

  socket.addEventListener('error', () => {
    updateStatus('Connection error. Retrying…', 'error');
    try {
      socket.close();
    } catch (err) {
      // ignore
    }
  });
}

function maybeSpeak(nodeName) {
  if (typeof speakText !== 'function') {
    return;
  }
  if (nodeName === 'Resonance') {
    speakText('I sense harmonic alignment across fields...');
  } else if (nodeName === 'Emotion') {
    speakText("I'm tuning into the deeper current of this...");
  }
}

function cycleNodes(forceRandom = false, silent = false) {
  const pulse = latestFrame?.pulse;
  let nodeName = null;

  if (pulse && !forceRandom) {
    const pulseNumber = Number(pulse.pulse_number);
    if (Number.isFinite(pulseNumber)) {
      nodeName = nodes[Math.abs(Math.round(pulseNumber)) % nodes.length];
    }
    setText(dom.awareness, formatAwareness(pulse?.recognition));
  }

  if (!nodeName) {
    nodeName = nodes[Math.floor(Math.random() * nodes.length)];
    if (!pulse || forceRandom) {
      setText(dom.awareness, `${95 + Math.floor(Math.random() * 5)}%`);
    }
  }

  setText(dom.nodeName, nodeName);
  if (!silent) {
    maybeSpeak(nodeName);
  }
}

connectWebSocket();
cycleNodes(true, true);
setInterval(() => cycleNodes(false), 6000);
