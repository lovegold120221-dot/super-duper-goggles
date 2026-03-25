#!/usr/bin/env python3
"""
Simplified Voice Agent for Eburon Voice Core
Works with LiveKit Agents v1.5.1
"""
import asyncio
import logging
from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli
from livekit.agents.voice import Agent
from livekit.agents.stt import STT
from livekit.agents.tts import TTS
from livekit.agents.vad import VAD
from livekit.agents.llm import LLM
from coqui_tts_plugin import CoquiXTTS

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimpleVoiceAgent(Agent):
    def __init__(self):
        super().__init__(
            vad=VAD(),
            stt=STT.with_model("whisper-1"),
            llm=LLM.with_model("llama3:latest"),
            tts=CoquiXTTS(),
            allow_interruptions=True
        )

async def entrypoint(ctx: JobContext):
    """Main entrypoint for the voice agent"""
    logger.info("Starting Eburon Voice Core Agent...")
    
    # Connect to the LiveKit Room
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)
    logger.info("Connected to LiveKit room")
    
    # Create and start the agent
    agent = SimpleVoiceAgent()
    agent.start(ctx.room)
    logger.info("Voice agent started")
    
    # Greet the caller
    await agent.say("Hi, thank you for calling Eburon support. How can I help you today?", 
                  allow_interruptions=True)
    logger.info("Greeting sent, waiting for user input...")

if __name__ == "__main__":
    logger.info("Initializing Eburon Voice Core...")
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
