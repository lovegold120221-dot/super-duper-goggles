#!/bin/bash

# Eburon Voice Core Setup Script
echo "Setting up Eburon Voice Core..."

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Setup Coqui TTS
echo "Setting up Coqui TTS..."
cd TTS
source ../venv/bin/activate
pip install -e .[all]
cd ..

echo "Setup complete! Follow these steps to run the system:"
echo "1. Start Docker and run: cd sip && docker compose up -d"
echo "2. Start Coqui TTS server: cd TTS && python -m TTS.demos.xtts_ft_demo.xtts_api_server --listen 0.0.0.0:8002 --model_name tts_models/multilingual/multi-dataset/xtts_v2"
echo "3. Start Ollama: ollama serve"
echo "4. Start voice agent: python voice_agent.py"
