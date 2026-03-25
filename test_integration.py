#!/usr/bin/env python3
"""
Complete Integration Test for Eburon Voice Core
Tests frontend-backend connectivity and API functionality
"""

import requests
import json
import time

def test_api_endpoint(url, method='GET', data=None, description=""):
    """Test an API endpoint and return results"""
    try:
        print(f"🧪 Testing: {description}")
        print(f"   URL: {method} {url}")
        
        if method == 'POST' and data:
            response = requests.post(url, json=data, timeout=5)
        else:
            response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            print(f"   ✅ SUCCESS ({response.status_code})")
            if response.headers.get('content-type', '').startswith('application/json'):
                json_data = response.json()
                print(f"   📊 Response: {json.dumps(json_data, indent=6)[:200]}...")
            return True
        else:
            print(f"   ❌ FAILED ({response.status_code})")
            print(f"   📄 Response: {response.text[:200]}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"   ❌ ERROR: {str(e)}")
        return False

def main():
    print("🚀 Eburon Voice Core - Complete Integration Test")
    print("=" * 50)
    
    # Test configuration
    tests = [
        # Frontend tests
        {
            'url': 'http://localhost:3004',
            'method': 'GET',
            'description': 'Frontend Dashboard (HTML)'
        },
        {
            'url': 'http://localhost:3004/api/sip/status',
            'method': 'GET', 
            'description': 'Frontend Proxy → SIP Gateway Status'
        },
        {
            'url': 'http://localhost:3004/api/sip/call',
            'method': 'POST',
            'data': {'from': '+1555123456', 'to': '+18005551234'},
            'description': 'Frontend Proxy → Test Call'
        },
        
        # Direct backend tests
        {
            'url': 'http://localhost:5060/api/status',
            'method': 'GET',
            'description': 'Direct SIP Gateway Status'
        },
        {
            'url': 'http://localhost:8002/health',
            'method': 'GET',
            'description': 'Direct TTS Server Health'
        },
        {
            'url': 'http://localhost:11434/api/tags',
            'method': 'GET',
            'description': 'Direct Ollama LLM Status'
        }
    ]
    
    # Run all tests
    results = []
    for test in tests:
        result = test_api_endpoint(
            url=test['url'],
            method=test['method'],
            data=test.get('data'),
            description=test['description']
        )
        results.append(result)
        print()  # Add spacing between tests
    
    # Summary
    passed = sum(results)
    total = len(results)
    
    print("📊 Test Results Summary")
    print("=" * 30)
    print(f"✅ Passed: {passed}/{total}")
    print(f"❌ Failed: {total - passed}/{total}")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
        print("🚀 Your Eburon Voice Core system is fully integrated and working!")
        print("\n🌐 Access your dashboard at: http://localhost:3004")
        print("📞 Test calls work through the frontend interface")
        print("🔗 All services are properly connected")
    else:
        print("\n⚠️ Some tests failed. Check the errors above.")
        print("🔧 Make sure all services are running:")
        print("   - Ollama: ollama serve")
        print("   - SIP Gateway: python simplified_voice_core.py")
        print("   - TTS Server: python simple_tts_server.py")
        print("   - Frontend Proxy: cd frontend && python proxy_server.py")
    
    return passed == total

if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)
