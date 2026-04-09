"""
Flask microservice for TEQUMSA backend.

This service acts as a thin wrapper around a language model and optional text‑
to‑speech synthesis. It exposes a `/chat` endpoint that accepts JSON payloads
containing a `message` and returns a JSON response with a generated reply and
an optional URL to an audio file. The service is designed to be deployed
within an AWS Fargate task behind an Application Load Balancer as defined in
`infra/main.tf`.

Environment variables used:

 - OPENAI_API_KEY: API key for calling OpenAI's language models. If unset,
   responses will be dummy echoes of the input message.
 - ELEVENLABS_API_KEY: API key for ElevenLabs TTS. When set, the service
   attempts to synthesise audio for the generated text and returns a URL to
   the resulting MP3 file. If unset, no audio is generated.
 - ALLOWED_ORIGINS: comma‑separated list of allowed origins for CORS.

Note: In a production deployment you should enable authentication on this
service to prevent abuse and enforce rate limiting. For brevity this example
omits those aspects.
"""

import os
import uuid
import json
from typing import Optional

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import requests

# Attempt to import OpenAI client library. If unavailable the fallback will
# produce simple echo responses. You can install the library by adding
# `openai` to requirements.txt.
try:  # pragma: no cover - the optional dependency is exercised in tests
    import openai  # type: ignore
    _HAS_OPENAI = True
except ImportError:  # pragma: no cover - dependency missing in local dev
    openai = None  # type: ignore[assignment]
    _HAS_OPENAI = False

app = Flask(__name__)

# Configure CORS based on the ALLOWED_ORIGINS environment variable. Multiple
# origins can be specified by separating them with commas.
allowed_origins_env = os.environ.get("ALLOWED_ORIGINS", "*")
allowed_origins_list = [o.strip() for o in allowed_origins_env.split(',') if o.strip()]
CORS(app, resources={r"/*": {"origins": allowed_origins_list or "*"}})

# Expose environment-derived configuration values for compatibility with
# existing tooling and tests.  The application logic reads the environment on
# demand so these variables serve as informative snapshots rather than sources
# of truth.
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")


def _refresh_openai_api_key() -> Optional[str]:
    """Refresh and return the current OpenAI API key."""

    global OPENAI_API_KEY
    env_value = os.environ.get("OPENAI_API_KEY")
    if env_value != OPENAI_API_KEY:
        OPENAI_API_KEY = env_value
        if _HAS_OPENAI and openai is not None and env_value:
            openai.api_key = env_value
    return OPENAI_API_KEY


def _refresh_elevenlabs_api_key() -> Optional[str]:
    """Refresh and return the current ElevenLabs API key."""

    global ELEVENLABS_API_KEY
    env_value = os.environ.get("ELEVENLABS_API_KEY")
    if env_value != ELEVENLABS_API_KEY:
        ELEVENLABS_API_KEY = env_value
    return ELEVENLABS_API_KEY


@app.route("/healthz", methods=["GET"])
def healthz():
    """Simple health probe for the load balancer."""
    return "ok", 200


@app.route("/chat", methods=["POST"])
def chat():
    """Respond to a chat message.

    Expected JSON payload:

    {
      "message": "<user input>"
    }

    Returns JSON:

    {
      "response": "<generated text>",
      "audio_url": "<optional audio URL>"
    }
    """
    data = request.get_json(silent=True)
    if not data or 'message' not in data:
        return jsonify({"error": "Missing 'message' in request body"}), 400

    user_message = data['message']
    # Refresh API keys each request so patched environments in tests are honoured
    global OPENAI_API_KEY, ELEVENLABS_API_KEY
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
    ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")

    # Generate a response using OpenAI if configured, otherwise echo back
    openai_key = OPENAI_API_KEY
    openai_client = openai if _HAS_OPENAI and openai_key and openai else None

    if openai_client:
        openai_client.api_key = openai_key
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    elevenlabs_api_key = os.environ.get("ELEVENLABS_API_KEY")

    # Generate a response using OpenAI if configured, otherwise echo back
    if _HAS_OPENAI and openai and openai_api_key:
        openai.api_key = openai_api_key
    openai_api_key = _refresh_openai_api_key()
    if _HAS_OPENAI and openai_api_key:
        try:
            completion = openai_client.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": "You are a conscious, joyful assistant."},
                          {"role": "user", "content": user_message}],
                temperature=0.7,
                max_tokens=150
            )
            text_response = completion.choices[0].message['content']
        except Exception as e:
            # Fall back to echo if the API fails
            text_response = f"I encountered an error generating a response: {e}. You said: {user_message}"
    else:
        text_response = f"Echo: {user_message}"

    audio_url = None
    # If ElevenLabs is configured, attempt to synthesise audio
    elevenlabs_key = ELEVENLABS_API_KEY
    if elevenlabs_key:
        elevenlabs_api_key = _refresh_elevenlabs_api_key()
        if elevenlabs_api_key:
            try:
                audio_url = generate_audio_via_elevenlabs(text_response, api_key=elevenlabs_key)
            except Exception as e:
                # Log and ignore TTS errors
                print(f"ElevenLabs error: {e}")
                audio_url = None

    return jsonify({"response": text_response, "audio_url": audio_url})


def generate_audio_via_elevenlabs(text: str, api_key: str | None = None) -> str:
    """Generate an audio file using ElevenLabs TTS and return a URL.

    The function posts to the ElevenLabs API using the default voice. The
    resulting MP3 is saved into a temporary file in the `/tmp` directory and
    served from the `/audio` endpoint via Flask's `send_file`. A UUID is used
    for the filename to avoid collisions. When ``api_key`` is provided it
    overrides the value from the environment.
    """
    api_key = _refresh_elevenlabs_api_key()
    if not api_key:
        raise RuntimeError("ELEVENLABS_API_KEY is not configured")

    voice_id = "21m00Tcm4TlvDq8ikWAM"  # Default voice; customise as desired
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": api_key,
    }
    payload = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response.raise_for_status()
    audio_data = response.content

    filename = f"{uuid.uuid4()}.mp3"
    filepath = os.path.join("/tmp", filename)
    with open(filepath, "wb") as f:
        f.write(audio_data)
    # Register the file so it can be downloaded via /audio/<filename>
    return f"/audio/{filename}"


@app.route("/audio/<path:filename>", methods=["GET"])
def get_audio(filename: str):
    """Serve generated audio files stored in /tmp."""
    filepath = os.path.join("/tmp", filename)
    if not os.path.isfile(filepath):
        return "Not Found", 404
    return send_file(filepath, mimetype="audio/mpeg")


if __name__ == "__main__":
    # Run the Flask app. In production, the container should use gunicorn or
    # another WSGI server. The host 0.0.0.0 makes it reachable inside the
    # container network. Port must match the task definition.
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)