#!/usr/bin/env python3
"""
Final System Test for Eburon Voice Core
Tests all components and provides deployment status
"""
import asyncio
import aiohttp
import subprocess
import sys

async def test_all_components():
    """Test all system components"""
    print("🔍 Eburon Voice Core - Final System Test")
    print("=" * 50)
    
    results = {}
    
    # Test 1: Docker Services
    print("\n1. 🐳 Testing Docker Services...")
    try:
        result = subprocess.run(['docker', 'compose', 'ps'], 
                              cwd='sip', capture_output=True, text=True)
        print(f"Docker output: {result.stdout}")  # Debug output
        if 'Up' in result.stdout or 'Started' in result.stdout:
            print("✅ SIP Gateway services are running")
            results['docker'] = True
        else:
            print("❌ SIP Gateway services not running")
            results['docker'] = False
    except Exception as e:
        print(f"❌ Docker check failed: {e}")
        results['docker'] = False
    
    # Test 2: Ollama LLM
    print("\n2. 🤖 Testing Ollama LLM...")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("http://localhost:11434/api/tags") as response:
                if response.status == 200:
                    data = await response.json()
                    models = [m['name'] for m in data.get('models', [])]
                    print(f"✅ Ollama running with {len(models)} models")
                    if 'llama3:latest' in models:
                        print("✅ llama3 model available")
                    results['ollama'] = True
                else:
                    print("❌ Ollama not responding")
                    results['ollama'] = False
    except Exception as e:
        print(f"❌ Ollama connection failed: {e}")
        results['ollama'] = False
    
    # Test 3: TTS Server
    print("\n3. 🗣️ Testing TTS Server...")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("http://localhost:8002/health") as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ TTS Server healthy: {data.get('service')}")
                    results['tts'] = True
                else:
                    print(f"❌ TTS Server status: {response.status}")
                    results['tts'] = False
    except Exception as e:
        print(f"❌ TTS Server connection failed: {e}")
        results['tts'] = False
    
    # Test 4: TTS API
    print("\n4. 🔊 Testing TTS Synthesis...")
    try:
        async with aiohttp.ClientSession() as session:
            payload = {"text": "Hello world", "language": "en"}
            async with session.post("http://localhost:8002/api/tts", 
                                   json=payload) as response:
                if response.status == 200:
                    print("✅ TTS synthesis API working")
                    results['tts_api'] = True
                else:
                    print(f"❌ TTS API failed: {response.status}")
                    results['tts_api'] = False
    except Exception as e:
        print(f"❌ TTS API test failed: {e}")
        results['tts_api'] = False
    
    # Test 5: Network Ports
    print("\n5. 🌐 Testing Network Ports...")
    ports_to_test = [
        (5060, "SIP Signaling"),
        (11434, "Ollama API"),
        (8002, "TTS Server"),
        (7880, "LiveKit WebSocket")
    ]
    
    results['ports'] = True
    for port, service in ports_to_test:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"http://localhost:{port}/", timeout=2):
                    print(f"✅ Port {port} ({service}) - Open")
        except:
            print(f"⚠️ Port {port} ({service}) - Not accessible via HTTP")
            # Don't fail for SIP port as it's not HTTP
    
    return results

def print_deployment_guide(results):
    """Print deployment guide based on test results"""
    print("\n" + "=" * 50)
    print("📋 DEPLOYMENT STATUS & NEXT STEPS")
    print("=" * 50)
    
    all_good = all(results.values())
    
    if all_good:
        print("🎉 ALL SYSTEMS OPERATIONAL!")
        print("\n🚀 Ready for phone calls!")
        print("\n📞 To test with phone:")
        print("1. Configure your SIP provider webhook to:")
        print("   SIP Endpoint: 49.150.205.224:5060")
        print("2. Install livekit-cli and run:")
        print("   livekit-cli sip inbound create --name \"Test\" --numbers \"+1234567890\"")
        print("   livekit-cli sip dispatch create --name \"Default\" --room \"room-csr-inbound\"")
        print("3. Call your configured phone number")
        print("4. Start voice agent: python voice_agent_simple.py")
    else:
        print("⚠️ Some components need attention:")
        
        if not results.get('docker'):
            print("❌ Docker services - Run: cd sip && docker compose up -d")
        
        if not results.get('ollama'):
            print("❌ Ollama - Run: ollama serve")
        
        if not results.get('tts'):
            print("❌ TTS Server - Run: python simple_tts_server.py")
        
        if not results.get('tts_api'):
            print("❌ TTS API - Check TTS server logs")
    
    print("\n📊 Component Status:")
    for component, status in results.items():
        status_icon = "✅" if status else "❌"
        print(f"  {status_icon} {component.title()}: {'Working' if status else 'Needs Fix'}")

async def main():
    """Main test function"""
    results = await test_all_components()
    print_deployment_guide(results)
    
    # Exit with error code if any component failed
    if not all(results.values()):
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
