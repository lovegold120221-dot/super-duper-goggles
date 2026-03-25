#!/bin/bash

# Eburon Voice Core - Complete System Startup
# This script starts all services needed for the voice AI system

echo "🚀 Starting Eburon Voice Core System..."
echo "=================================="

# Function to check if port is in use
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null ; then
        echo "✅ Port $1 is in use"
        return 0
    else
        echo "❌ Port $1 is free"
        return 1
    fi
}

# Function to wait for service to be ready
wait_for_service() {
    local url=$1
    local service_name=$2
    local max_attempts=30
    local attempt=1
    
    echo "⏳ Waiting for $service_name to be ready..."
    while [ $attempt -le $max_attempts ]; do
        if curl -s "$url" >/dev/null 2>&1; then
            echo "✅ $service_name is ready!"
            return 0
        fi
        echo "   Attempt $attempt/$max_attempts..."
        sleep 2
        ((attempt++))
    done
    
    echo "❌ $service_name failed to start"
    return 1
}

# Check if required services are running
echo "🔍 Checking service status..."

# Check Ollama (port 11434)
if check_port 11434; then
    echo "✅ Ollama is running"
else
    echo "❌ Ollama is not running. Please start Ollama first:"
    echo "   ollama serve"
    exit 1
fi

# Check SIP Gateway (port 5060)
if ! check_port 5060; then
    echo "🔧 Starting SIP Gateway..."
    source venv/bin/activate
    python simplified_voice_core.py &
    SIP_PID=$!
    echo "📡 SIP Gateway starting (PID: $SIP_PID)"
    
    # Wait for SIP Gateway to be ready
    if ! wait_for_service "http://localhost:5060/api/status" "SIP Gateway"; then
        echo "❌ SIP Gateway failed to start"
        kill $SIP_PID 2>/dev/null
        exit 1
    fi
else
    echo "✅ SIP Gateway is already running"
fi

# Check TTS Server (port 8002)
if ! check_port 8002; then
    echo "🔧 Starting TTS Server..."
    source venv/bin/activate
    python simple_tts_server.py &
    TTS_PID=$!
    echo "🗣️ TTS Server starting (PID: $TTS_PID)"
    
    # Wait for TTS Server to be ready
    if ! wait_for_service "http://localhost:8002/health" "TTS Server"; then
        echo "❌ TTS Server failed to start"
        kill $TTS_PID 2>/dev/null
        exit 1
    fi
else
    echo "✅ TTS Server is already running"
fi

# Start Frontend with Proxy (port 3004)
if ! check_port 3004; then
    echo "🔧 Starting Frontend with API Proxy..."
    cd frontend
    python proxy_server.py &
    FRONTEND_PID=$!
    echo "🌐 Frontend Proxy starting (PID: $FRONTEND_PID)"
    
    # Wait for Frontend to be ready
    if ! wait_for_service "http://localhost:3004/api/sip/status" "Frontend Proxy"; then
        echo "❌ Frontend Proxy failed to start"
        kill $FRONTEND_PID 2>/dev/null
        exit 1
    fi
else
    echo "✅ Frontend Proxy is already running"
fi

# Show system status
echo ""
echo "🎉 Eburon Voice Core System is READY!"
echo "==================================="
echo "🌐 Frontend Dashboard: http://localhost:3004"
echo "📊 API Status: http://localhost:3004/api/sip/status"
echo "📞 Test Call: POST http://localhost:3004/api/sip/call"
echo ""
echo "🔧 Service URLs:"
echo "   - SIP Gateway: http://localhost:5060"
echo "   - TTS Server:  http://localhost:8002"
echo "   - Ollama LLM:   http://localhost:11434"
echo ""
echo "📱 Open your browser and navigate to:"
echo "   http://localhost:3004"
echo ""
echo "🛑 To stop the system, press Ctrl+C"

# Save PIDs for cleanup
echo $SIP_PID > .sip_pid
echo $TTS_PID > .tts_pid  
echo $FRONTEND_PID > .frontend_pid

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping Eburon Voice Core System..."
    
    if [ -f .sip_pid ]; then
        SIP_PID=$(cat .sip_pid)
        kill $SIP_PID 2>/dev/null && echo "✅ SIP Gateway stopped"
        rm .sip_pid
    fi
    
    if [ -f .tts_pid ]; then
        TTS_PID=$(cat .tts_pid)
        kill $TTS_PID 2>/dev/null && echo "✅ TTS Server stopped"
        rm .tts_pid
    fi
    
    if [ -f .frontend_pid ]; then
        FRONTEND_PID=$(cat .frontend_pid)
        kill $FRONTEND_PID 2>/dev/null && echo "✅ Frontend Proxy stopped"
        rm .frontend_pid
    fi
    
    echo "👋 System stopped. Goodbye!"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Keep script running
echo "⏰ System is running. Monitoring services..."
while true; do
    sleep 30
    
    # Check if services are still running
    if ! check_port 5060; then
        echo "⚠️ SIP Gateway stopped unexpectedly!"
        break
    fi
    
    if ! check_port 8002; then
        echo "⚠️ TTS Server stopped unexpectedly!"
        break
    fi
    
    if ! check_port 3004; then
        echo "⚠️ Frontend Proxy stopped unexpectedly!"
        break
    fi
done

cleanup
