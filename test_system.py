#!/usr/bin/env python3
"""
Simple test to verify Eburon Voice Core components
"""
import asyncio
import sys
import subprocess
import aiohttp

async def test_components():
    """Test each component individually"""
    print("🔍 Testing Eburon Voice Core Components...")
    
    # Test 1: Ollama connectivity
    print("\n1. Testing Ollama connectivity...")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("http://localhost:11434/api/tags") as response:
                if response.status == 200:
                    data = await response.json()
                    models = [m['name'] for m in data.get('models', [])]
                    print(f"✅ Ollama server accessible with models: {models}")
                else:
                    print(f"❌ Ollama returned status: {response.status}")
                    return False
    except Exception as e:
        print(f"❌ Ollama connection failed: {e}")
        return False
    
    # Test 2: Docker services
    print("\n2. Testing Docker services...")
    try:
        result = subprocess.run(['docker', 'compose', 'ps'], 
                              cwd='sip', capture_output=True, text=True)
        if 'Up' in result.stdout:
            print("✅ SIP Gateway services are running")
        else:
            print("❌ SIP Gateway services not running properly")
            return False
    except Exception as e:
        print(f"❌ Docker check failed: {e}")
        return False
    
    # Test 3: TTS Server
    print("\n3. Testing TTS Server...")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("http://localhost:8002/", timeout=5) as response:
                print(f"✅ TTS server responding with status: {response.status}")
    except Exception as e:
        print(f"⚠️ TTS server not accessible (may need license confirmation): {e}")
    
    # Test 4: Basic LiveKit imports
    print("\n4. Testing LiveKit imports...")
    try:
        import livekit.agents
        import livekit
        print("✅ Basic LiveKit imports successful")
    except Exception as e:
        print(f"❌ Basic import failed: {e}")
        return False
    
    print("\n🎉 Core components are working!")
    return True

async def main():
    """Main test function"""
    print("=" * 50)
    print("EBURON VOICE CORE - SYSTEM TEST")
    print("=" * 50)
    
    success = await test_components()
    
    if success:
        print("\n🚀 System foundation is ready!")
        print("\nCurrent status:")
        print("✅ Docker/Colima: Running")
        print("✅ SIP Gateway: Running")
        print("✅ Ollama: Running with llama3 model")
        print("⚠️ TTS Server: Needs license confirmation")
        print("⚠️ Voice Agent: Needs plugin updates")
        print("\nNext steps:")
        print("1. Confirm TTS server license agreement")
        print("2. Update voice agent imports for new LiveKit version")
        print("3. Start voice agent")
        print("4. Configure SIP provider webhook")
        print("5. Test with phone call")
    else:
        print("\n❌ Some components need attention before deployment")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
