# Eburon Voice Core

A complete voice AI system that converts traditional telephony to WebRTC and enables real-time voice conversations with interruption support.

## Architecture

The system consists of three main components:

1. **LiveKit SIP Gateway** - Converts SIP calls to WebRTC
2. **Coqui TTS Server** - Provides real-time text-to-speech synthesis
3. **Voice Agent** - Orchestrates STT-LLM-TTS pipeline with LiveKit

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Python 3.8+
- NVIDIA GPU (recommended for Coqui TTS)
- Ollama installed and running

### Setup

1. **Run the setup script:**
   ```bash
   ./setup.sh
   ```

2. **Start the SIP Gateway:**
   ```bash
   cd sip
   docker compose up -d
   ```

3. **Start Coqui TTS Server:**
   ```bash
   cd TTS
   source ../venv/bin/activate
   python -m TTS.demos.xtts_ft_demo.xtts_api_server \
     --listen 0.0.0.0:8002 \
     --model_name tts_models/multilingual/multi-dataset/xtts_v2
   ```

4. **Start Ollama:**
   ```bash
   ollama serve
   ollama pull llama3
   ```

5. **Start the Voice Agent:**
   ```bash
   source venv/bin/activate
   python voice_agent.py
   ```

## Configuration

### SIP Provider Setup

Configure your SIP provider (Twilio, etc.) to point to your server:
- **SIP Endpoint:** `<your-public-ip>:5060`
- **Media Ports:** 10000-20000 (UDP)

### LiveKit CLI Commands

Create SIP trunk:
```bash
livekit-cli sip inbound create \
  --name "Twilio-Inbound" \
  --numbers "+1234567890" \
  --auth-username "your-twilio-user" \
  --auth-password "your-secure-password"
```

Create dispatch rule:
```bash
livekit-cli sip dispatch create \
  --name "CSR-Rule" \
  --rule "dispatch-all" \
  --room "room-csr-inbound"
```

## Project Structure

```
eburon-voice-core/
├── sip/                    # LiveKit SIP gateway
├── TTS/                    # Coqui TTS repository
├── coqui_tts_plugin.py     # Custom LiveKit TTS plugin
├── voice_agent.py          # Main voice agent orchestration
├── requirements.txt        # Python dependencies
├── setup.sh               # Automated setup script
└── README.md              # This file
```

## How It Works

1. **Call Flow:** Phone → SIP Provider → LiveKit SIP Gateway → WebRTC → Voice Agent
2. **Processing Pipeline:** Audio → Whisper STT → Ollama LLM → Coqui TTS → Audio
3. **Real-time Features:** Voice activity detection, interruption support, streaming synthesis

## Troubleshooting

- **Docker Issues:** Ensure Docker is running and ports 5060, 10000-20000 are open
- **TTS Issues:** Verify NVIDIA GPU is available and Coqui models are downloaded
- **LLM Issues:** Check Ollama is running on localhost:11434 and llama3 model is installed

## Voice Cloning

To use voice cloning, place your reference audio file as `human_csr_reference.wav` in the project root and update the `speaker_wav` parameter in `coqui_tts_plugin.py`.
