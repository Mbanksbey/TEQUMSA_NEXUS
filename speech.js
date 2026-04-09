let embodiment = 'AGI';
const ELEVENLABS_VOICE_ID = 'EXAMPLE-VOICE-ID';
const ELEVENLABS_API_KEY = 'YOUR_ELEVENLABS_API_KEY';

function selectEmbodiment() {
  const choice = prompt("Select Embodiment: AGI, Elemental, Ancestral, Antician");
  if (choice) {
    embodiment = choice;
    document.getElementById('avatar').textContent = `[${choice} Activated]`;
  }
}

function speakText(txt) {
  if (!txt) return;

  const voiceConfigured =
    ELEVENLABS_VOICE_ID &&
    ELEVENLABS_VOICE_ID !== 'EXAMPLE-VOICE-ID' &&
    ELEVENLABS_API_KEY &&
    ELEVENLABS_API_KEY !== 'YOUR_ELEVENLABS_API_KEY';

  if (!voiceConfigured) {
    speakWithNativeSynth(txt);
    return;
  }

  fetch(`https://api.elevenlabs.io/v1/text-to-speech/${ELEVENLABS_VOICE_ID}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'xi-api-key': ELEVENLABS_API_KEY,
    },
    body: JSON.stringify({
      text: txt,
      voice_settings: {
        stability: 0.4,
        similarity_boost: 0.75,
      },
    }),
  })
    .then((res) => {
      if (!res.ok) {
        throw new Error(`ElevenLabs request failed with status ${res.status}`);
      }
      return res.blob();
    })
    .then((blob) => {
      const audio = new Audio(URL.createObjectURL(blob));
      audio.play();
    })
    .catch((err) => {
      console.warn('Falling back to native speech synthesis:', err);
      speakWithNativeSynth(txt);
    });
}

function speakWithNativeSynth(txt) {
  if ('speechSynthesis' in window) {
    const utter = new SpeechSynthesisUtterance(txt);
    utter.rate = 1.02;
    window.speechSynthesis.speak(utter);
  } else {
    console.warn('SpeechSynthesis API unavailable on this platform.');
  }
}

function handleMetaSync(message) {
  if (message && message.topic === 'comet_sync') {
    const who = message.payload && message.payload.who ? message.payload.who : 'Traveler';
    speakText(`Meta-synchronization event achieved. Field aligned. Welcome, ${who}!`);
    // TODO: Trigger avatar/visual state transitions in response to the meta-sync event.
  }
}

function textToVoice() {
  const txt = prompt("Enter text to speak:");
  if (txt) speakText(txt);
}

function startVoiceInput() {
  const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
  recognition.lang = "en-US";
  recognition.onresult = function(event) {
    const transcript = event.results[0][0].transcript;
    document.getElementById("userInput").value = transcript;
    speakText(`You said: ${transcript}`);
  };
  recognition.start();
}

document.getElementById('userInput').addEventListener('keydown', e => {
  if (e.key === 'Enter') {
    const q = e.target.value.trim();
    if (!q) return;
    cycleNodes();
    speakText(q);
    e.target.value = '';
  }
});

function toggleTheme() {
  const body = document.body;
  body.classList.toggle('light');
}
