#!/bin/bash

# Eburon Voice Core - Stop All Services
echo "Stopping Eburon Voice Core Services..."

# Stop Voice Agent
if [ -f "voice-agent.pid" ]; then
    pid=$(cat voice-agent.pid)
    if ps -p $pid > /dev/null; then
        kill $pid
        echo "Stopped Voice Agent (PID: $pid)"
    fi
    rm voice-agent.pid
fi

# Stop Coqui TTS
if [ -f "coqui-tts.pid" ]; then
    pid=$(cat coqui-tts.pid)
    if ps -p $pid > /dev/null; then
        kill $pid
        echo "Stopped Coqui TTS (PID: $pid)"
    fi
    rm coqui-tts.pid
fi

# Stop Ollama
if [ -f "ollama.pid" ]; then
    pid=$(cat ollama.pid)
    if ps -p $pid > /dev/null; then
        kill $pid
        echo "Stopped Ollama (PID: $pid)"
    fi
    rm ollama.pid
fi

# Stop SIP Gateway
cd sip
docker compose down
echo "Stopped SIP Gateway"
cd ..

echo ""
echo "✅ All Eburon Voice Core services have been stopped."
