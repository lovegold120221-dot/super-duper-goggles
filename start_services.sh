#!/bin/bash

# Eburon Voice Core - Complete System Startup
echo "Starting Eburon Voice Core System..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "Error: Docker is not running. Please start Docker first."
    exit 1
fi

# Function to start a service in background
start_service() {
    local service_name=$1
    local command=$2
    local log_file="${service_name}.log"
    
    echo "Starting $service_name..."
    eval "$command" > "$log_file" 2>&1 &
    local pid=$!
    echo "$service_name started with PID: $pid (logs: $log_file)"
    echo $pid > "${service_name}.pid"
}

# Start SIP Gateway
cd sip
docker compose up -d
echo "SIP Gateway started via Docker Compose"
cd ..

# Start Coqui TTS Server
start_service "coqui-tts" "cd TTS && source ../venv/bin/activate && python -m TTS.demos.xtts_ft_demo.xtts_api_server --listen 0.0.0.0:8002 --model_name tts_models/multilingual/multi-dataset/xtts_v2"

# Wait a moment for TTS to initialize
sleep 5

# Start Ollama (if not already running)
if ! pgrep -f "ollama serve" > /dev/null; then
    start_service "ollama" "ollama serve"
    sleep 3
fi

# Start Voice Agent
start_service "voice-agent" "source venv/bin/activate && python voice_agent.py"

echo ""
echo "🎉 Eburon Voice Core is starting up!"
echo ""
echo "Service Status:"
echo "- SIP Gateway: Running via Docker"
echo "- Coqui TTS: Starting (port 8002)"
echo "- Ollama: Starting (port 11434)"
echo "- Voice Agent: Starting"
echo ""
echo "Check the .log files for service status:"
echo "tail -f coqui-tts.log"
echo "tail -f ollama.log"
echo "tail -f voice-agent.log"
echo ""
echo "To stop all services, run: ./stop_services.sh"
