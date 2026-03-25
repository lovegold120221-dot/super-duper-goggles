#!/usr/bin/env python3
"""
Complete System Test - Eburon Voice Core (Simplified Mode)
Tests all components without Docker dependency
"""
import asyncio
import aiohttp
import subprocess
import sys

async def test_complete_system():
    """Test all system components"""
    print("🎯 Eburon Voice Core - Complete System Test")
    print("=" * 60)
    
    results = {}
    
    # Test 1: Simulated SIP Gateway
    print("\n1. 📞 Testing Simulated SIP Gateway...")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("http://localhost:5060/api/status") as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ SIP Gateway running: {data.get('services', {}).get('sip_gateway')}")
                    results['sip_gateway'] = True
                else:
                    print(f"❌ SIP Gateway failed: {response.status}")
                    results['sip_gateway'] = False
    except Exception as e:
        print(f"❌ SIP Gateway connection failed: {e}")
        results['sip_gateway'] = False
    
    # Test 2: Call Simulation
    print("\n2. 📞 Testing Call Simulation...")
    try:
        async with aiohttp.ClientSession() as session:
            payload = {"from": "+1234567890", "to": "+0987654321"}
            async with session.post("http://localhost:5060/api/call", 
                                   json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ Call simulation successful: {data.get('call_id')}")
                    print(f"   Status: {data.get('status')}")
                    print(f"   Room: {data.get('room')}")
                    results['call_simulation'] = True
                else:
                    print(f"❌ Call simulation failed: {response.status}")
                    results['call_simulation'] = False
    except Exception as e:
        print(f"❌ Call simulation failed: {e}")
        results['call_simulation'] = False
    
    # Test 3: Ollama LLM
    print("\n3. 🤖 Testing Ollama LLM...")
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
    
    # Test 4: TTS Server
    print("\n4. 🗣️ Testing TTS Server...")
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
    
    # Test 5: TTS Synthesis
    print("\n5. 🔊 Testing TTS Synthesis...")
    try:
        async with aiohttp.ClientSession() as session:
            payload = {"text": "Hello from Eburon Voice Core", "language": "en"}
            async with session.post("http://localhost:8002/api/tts", 
                                   json=payload) as response:
                if response.status == 200:
                    print("✅ TTS synthesis API working")
                    results['tts_synthesis'] = True
                else:
                    print(f"❌ TTS synthesis failed: {response.status}")
                    results['tts_synthesis'] = False
    except Exception as e:
        print(f"❌ TTS synthesis failed: {e}")
        results['tts_synthesis'] = False
    
    # Test 6: Voice Agent Code
    print("\n6. 🤖 Testing Voice Agent Code...")
    try:
        import voice_agent_simple
        print("✅ Voice agent imports successful")
        results['voice_agent'] = True
    except Exception as e:
        print(f"❌ Voice agent import failed: {e}")
        results['voice_agent'] = False
    
    return results

def print_final_results(results):
    """Print comprehensive results"""
    print("\n" + "=" * 60)
    print("🏆 FINAL SYSTEM STATUS")
    print("=" * 60)
    
    all_good = all(results.values())
    
    if all_good:
        print("🎉 ALL SYSTEMS FULLY OPERATIONAL!")
        print("\n🚀 Eburon Voice Core is Ready for Production!")
        print("\n📞 How to Use:")
        print("1. Simulated SIP Gateway: http://localhost:5060")
        print("2. TTS Server: http://localhost:8002")
        print("3. Ollama LLM: http://localhost:11434")
        print("4. Voice Agent: python voice_agent_simple.py")
        print("\n🔧 Test Call Flow:")
        print("curl -X POST http://localhost:5060/api/call \\")
        print("  -H 'Content-Type: application/json' \\")
        print("  -d '{\"from\": \"+1234567890\", \"to\": \"+0987654321\"}'")
    else:
        print("⚠️ Some components need attention:")
        
        for component, status in results.items():
            status_icon = "✅" if status else "❌"
            print(f"  {status_icon} {component.replace('_', ' ').title()}: {'Working' if status else 'Needs Fix'}")
    
    print("\n📊 Success Rate:")
    working = sum(results.values())
    total = len(results)
    percentage = (working / total) * 100
    print(f"  {working}/{total} components working ({percentage:.1f}%)")
    
    print("\n🎯 Mission Status:")
    if percentage >= 90:
        print("  🏅 EXCELLENT - System ready for deployment!")
    elif percentage >= 75:
        print("  ✅ GOOD - Minor issues remaining")
    elif percentage >= 50:
        print("  ⚠️ FAIR - Some components need work")
    else:
        print("  ❌ POOR - Major issues to resolve")

async def main():
    """Main test function"""
    results = await test_complete_system()
    print_final_results(results)
    
    # Exit with appropriate code
    if not all(results.values()):
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
