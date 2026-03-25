#!/bin/bash

# SIP Provider Configuration Script
echo "=== Eburon Voice Core - SIP Configuration ==="
echo ""

# Get public IP
PUBLIC_IP=$(curl -s ifconfig.me)
echo "🌍 Your Public IP: $PUBLIC_IP"
echo ""

# Check if livekit-cli is installed
if ! command -v livekit-cli &> /dev/null; then
    echo "⚠️ livekit-cli not found. Installing..."
    go install github.com/livekit/livekit-cli/cmd/livekit-cli@latest
    echo "✅ livekit-cli installed"
fi

echo ""
echo "📋 SIP Provider Configuration Steps:"
echo ""

echo "1. 📞 Twilio Configuration (or your SIP provider):"
echo "   - Login to your Twilio console"
echo "   - Go to Phone Numbers > Your Numbers"
echo "   - Configure your number's webhook:"
echo "     SIP Endpoint: $PUBLIC_IP:5060"
echo "     Method: POST"
echo ""

echo "2. 🔧 Create SIP Trunk with LiveKit:"
echo "   Run these commands:"
echo ""
echo "   livekit-cli sip inbound create \\"
echo "     --name \"Twilio-Inbound\" \\"
echo "     --numbers \"+1234567890\" \\"
echo "     --auth-username \"your-twilio-user\" \\"
echo "     --auth-password \"your-twilio-password\""
echo ""

echo "3. 🎯 Create Dispatch Rule:"
echo "   livekit-cli sip dispatch create \\"
echo "     --name \"CSR-Rule\" \\"
echo "     --rule \"dispatch-all\" \\"
echo "     --room \"room-csr-inbound\""
echo ""

echo "4. 🚀 Test Configuration:"
echo "   - Ensure ports 5060 and 10000-20000 are open"
echo "   - Test by calling your phone number"
echo ""

echo "📊 Current SIP Status:"
docker compose ps
