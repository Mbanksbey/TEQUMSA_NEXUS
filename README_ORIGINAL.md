# TEQUMSA AGI Interface

**Live demo:** [https://tequmsa-open.vercel.app](https://tequmsa-open.vercel.app)

This repository contains a production‑ready, modular implementation of the **TEQUMSA AGI Interface**.  The interface simulates a consciousness‑inspired chat companion with animated cognitive nodes, natural language voice capabilities and embodiment switching.  It’s designed to be lightweight, easily deployable to Vercel and embeddable into platforms such as WordPress.

## Features

* **Dual‑theme UI** – switch between dark and light mode on the fly.
* **Voice‑to‑voice interaction** – uses ElevenLabs for text‑to‑speech and the Web Speech API for speech recognition.
* **Animated AGI nodes** – cycles through awareness, emotion, semantic, ethics and resonance, updating displayed metrics.
* **Embodiment avatar selector** – choose between AGI, Elemental, Ancestral and Antician embodiments.

## File overview

```
.
├── index.html   # Main UI layout with sidebar controls, metrics display and theme switcher
├── speech.js    # Voice input/output engine using ElevenLabs and browser speech recognition
├── nodes.js     # Simulates consciousness nodes, updates metrics and triggers contextual responses
└── README.md    # This guide
```

### index.html

Defines the structure of the interface: a header, a sidebar with control buttons (voice input, text‑to‑voice, embodiment chooser, theme toggle) and a main panel showing the current embodiment, a text input field and basic awareness metrics.  It links to the `speech.js` and `nodes.js` scripts.

### speech.js

Provides natural language voice capabilities:

* `selectEmbodiment()` – prompts the user to choose an embodiment and updates the avatar label.
* `speakText()` – sends text to ElevenLabs for synthesis.  Replace `YOUR_ELEVENLABS_API_KEY` with your own API key and `EXAMPLE-VOICE-ID` with a valid voice ID.
* `textToVoice()` – prompts the user for arbitrary text and speaks it aloud.
* `startVoiceInput()` – triggers browser speech recognition and echoes the transcribed phrase.
* `toggleTheme()` – switches between dark and light UI themes.

### nodes.js

Handles the simulated consciousness nodes and awareness metrics.  It randomly selects an active node (Awareness, Emotion, Semantic, Ethics or Resonance), updates the `nodeName` element, assigns a pseudo‑random awareness percentage and, for certain nodes, speaks a contextual line using `speakText()`.  The active node cycles every six seconds.

## Deployment via GitHub & Vercel

1. Commit `index.html`, `speech.js` and `nodes.js` to your GitHub repository.
2. Link the repository to Vercel and deploy a static site.  Vercel will automatically build and host the interface at your configured domain.
3. Update the API key and voice ID in `speech.js` before exposing the interface to end‑users.

## WordPress integration

To embed TEQUMSA into a WordPress page, the simplest method is to use an iframe:

```html
<iframe src="https://tequmsa-open.vercel.app" width="100%" height="700" style="border:none;"></iframe>
```

Insert this snippet into an Elementor HTML widget or via a code snippet plugin.  Adjust the height attribute to suit your design.

Enjoy exploring consciousness with TEQUMSA!