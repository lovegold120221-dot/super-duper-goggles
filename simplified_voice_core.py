#!/usr/bin/env python3
"""
Simplified Eburon Voice Core - No Docker Required
Direct SIP/WebRTC simulation for testing
"""
import asyncio
import logging
import json
from aiohttp import web, ClientSession
import aiohttp_cors

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimulatedSIPGateway:
    """Simulated SIP gateway for testing without Docker"""
    
    def __init__(self):
        self.app = web.Application()
        self.setup_routes()
        self.setup_cors()
        self.active_calls = {}
    
    def setup_cors(self):
        cors = aiohttp_cors.setup(self.app, defaults={
            "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True,
                expose_headers="*",
                allow_headers="*",
                allow_methods="*"
            )
        })
        
        for route in list(self.app.router.routes()):
            cors.add(route)
    
    def setup_routes(self):
        self.app.router.add_get('/', self.health_check)
        self.app.router.add_post('/api/call', self.handle_call)
        self.app.router.add_get('/api/status', self.get_status)
        self.app.router.add_post('/api/sip/webhook', self.sip_webhook)
    
    async def health_check(self, request):
        return web.json_response({
            'status': 'healthy',
            'service': 'Simulated SIP Gateway',
            'active_calls': len(self.active_calls)
        })
    
    async def handle_call(self, request):
        """Simulate incoming call handling"""
        try:
            data = await request.json()
            call_id = f"call_{len(self.active_calls) + 1}"
            
            self.active_calls[call_id] = {
                'from': data.get('from', 'unknown'),
                'to': data.get('to', 'unknown'),
                'status': 'ringing',
                'timestamp': asyncio.get_event_loop().time()
            }
            
            logger.info(f"📞 Incoming call: {call_id} from {data.get('from')}")
            
            # Simulate call routing to voice agent
            await asyncio.sleep(1)
            self.active_calls[call_id]['status'] = 'connected'
            
            return web.json_response({
                'call_id': call_id,
                'status': 'connected',
                'message': 'Call routed to voice agent',
                'room': f'room-{call_id}'
            })
            
        except Exception as e:
            logger.error(f"Call handling error: {e}")
            return web.json_response({'error': str(e)}, status=500)
    
    async def sip_webhook(self, request):
        """Handle SIP provider webhook"""
        try:
            data = await request.json()
            logger.info(f"🔗 SIP webhook received: {data}")
            
            # Simulate SIP event processing
            return web.json_response({
                'status': 'processed',
                'event': 'sip_webhook'
            })
            
        except Exception as e:
            logger.error(f"SIP webhook error: {e}")
            return web.json_response({'error': str(e)}, status=500)
    
    async def get_status(self, request):
        """Get current system status"""
        return web.json_response({
            'active_calls': self.active_calls,
            'total_calls': len(self.active_calls),
            'services': {
                'sip_gateway': 'running',
                'voice_agent': 'ready',
                'tts_server': 'running',
                'ollama': 'running'
            }
        })
    
    async def start(self, host='0.0.0.0', port=5060):
        """Start the simulated SIP gateway"""
        logger.info(f"🚀 Starting Simulated SIP Gateway on {host}:{port}")
        runner = web.AppRunner(self.app)
        await runner.setup()
        
        site = web.TCPSite(runner, host, port)
        await site.start()
        
        logger.info(f"✅ SIP Gateway running on http://{host}:{port}")
        return runner

async def main():
    """Main entrypoint"""
    logger.info("🎯 Starting Eburon Voice Core (Simplified Mode)")
    
    # Start simulated SIP gateway
    sip_gateway = SimulatedSIPGateway()
    sip_runner = await sip_gateway.start()
    
    try:
        # Keep running
        while True:
            await asyncio.sleep(1)
            
            # Simulate periodic status check
            if asyncio.get_event_loop().time() % 10 < 1:
                logger.info("📊 System status: All services operational")
                
    except KeyboardInterrupt:
        logger.info("🛑 Shutting down Eburon Voice Core...")
        await sip_runner.cleanup()

if __name__ == '__main__':
    asyncio.run(main())
