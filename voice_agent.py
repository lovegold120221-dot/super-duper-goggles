from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli
from livekit.agents.voice import Agent
from livekit.agents.stt import faster_whisper
from livekit.agents.tts import openai
from livekit.agents.vad import silero
# Import your custom Coqui class from Part 3 here
from coqui_tts_plugin import CoquiXTTS 

async def entrypoint(ctx: JobContext):
    # Connect to the LiveKit Room
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    # Instantiate the pipeline
    agent = Agent(
        vad=silero.VAD.load(),
        stt=faster_whisper.STT(), # Runs locally for fast real-time transcription
        llm=openai.LLM(
            base_url="http://localhost:11434/v1", # Your Ollama local server
            api_key="ollama",
            model="llama3:latest"
        ),
        tts=CoquiXTTS(), # <-- Your Custom Coqui Integration
        allow_interruptions=True, # Allows the caller to interrupt Coqui mid-sentence
    )

    # Start the agent and greet the phone caller
    agent.start(ctx.room)
    await agent.say("Hi, thank you for calling support. How can I help you today?", allow_interruptions=True)

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
