Develop Eburon Edge Voice following the steps below

Part 1: Setting up LiveKit SIP (livekit/sip)
This repository acts as the bridge translating standard telephone SIP traffic (from Twilio, SignalWire, etc.) into WebRTC audio for your LiveKit room[2].
1. Deploy the SIP GatewayThe easiest way to run the SIP server alongside LiveKit is using the docker-compose.yaml provided in their repository[3].
code Bash
downloadcontent_copy
expand_less
git clone https://github.com/livekit/sip.git
cd sip

# Start the SIP server, Redis, and a local LiveKit instance
docker compose up -d
(Note: Ensure ports 5060 (SIP Signaling) and 10000-20000 (UDP Media) are open on your server's firewall)[3].
2. Create a SIP Trunk (Inbound/Outbound)Using the livekit-cli, you need to authenticate your phone provider (e.g., Twilio) with your LiveKit SIP server[2].
code Bash
downloadcontent_copy
expand_less
livekit-cli sip inbound create \
  --name "Twilio-Inbound" \
  --numbers "+1234567890" \ # Your purchased phone number
  --auth-username "my-twilio-user" \
  --auth-password "my-secure-password"
3. Create a SIP Dispatch RuleThis tells LiveKit which "Room" to drop the phone caller into when they dial your number[2].
code Bash
downloadcontent_copy
expand_less
livekit-cli sip dispatch create \
  --name "CSR-Rule" \
  --rule "dispatch-all" \
  --room "room-csr-inbound" # The room your AI Agent will join

Part 2: Setting up Coqui TTS (coqui-ai/TTS)
To get sub-200ms real-time latency[4], you must use XTTSv2 in streaming mode.
1. Install Coqui TTSAs requested, you install this directly from the repository. It is highly recommended to do this on a machine with a dedicated NVIDIA GPU.
code Bash
downloadcontent_copy
expand_less
git clone https://github.com/coqui-ai/TTS.git
cd TTS
python3 -m venv venv
source venv/bin/activate

# Install with PyTorch and all dependencies
pip install -e .[all]
2. Start the XTTS Streaming ServerCoqui natively includes a streaming server designed specifically for XTTSv2. It exposes a WebSocket or HTTP endpoint that streams raw audio chunks as the text is generated.
code Bash
downloadcontent_copy
expand_less
# This starts a local server on port 8002
python -m TTS.demos.xtts_ft_demo.xtts_api_server \
  --listen 0.0.0.0:8002 \
  --model_name tts_models/multilingual/multi-dataset/xtts_v2

Part 3: The Missing Glue (Custom LiveKit TTS Class)
Because you are using a custom local model (coqui-ai/TTS), you must write a custom TTS class that inherits from livekit.agents.tts.TTS[1]. This intercepts the text stream from your Ollama LLM, sends it to Coqui, and yields AudioFrame objects to LiveKit.
Here is the blueprint for your custom Coqui XTTS LiveKit Plugin:
code Python
downloadcontent_copy
expand_less
import aiohttp
import asyncio
from livekit import rtc
from livekit.agents import tts

class CoquiXTTS(tts.TTS):
    def __init__(self):
        super().__init__(
            sample_rate=24000,
            num_channels=1,
            streaming_supported=True # Crucial for real-time
        )
        # Point to your local Coqui TTS server
        self.api_url = "http://localhost:8002/api/tts-stream" 

    def synthesize(self, text: str) -> tts.ChunkedStream:
        return CoquiStream(self.api_url, text)

class CoquiStream(tts.ChunkedStream):
    def __init__(self, api_url: str, text: str):
        super().__init__()
        self.api_url = api_url
        self.text = text

    async def _run(self):
        # Call the Coqui streaming endpoint
        async with aiohttp.ClientSession() as session:
            payload = {
                "text": self.text,
                "language": "en", # XTTS supports multilingual (es, fr, etc.)
                "speaker_wav": "human_csr_reference.wav" # Your voice clone target
            }
            async with session.post(self.api_url, json=payload) as response:
                # Read the audio bytes as Coqui streams them
                async for chunk in response.content.iter_chunked(4096):
                    # Convert raw bytes into LiveKit AudioFrames
                    audio_frame = rtc.AudioFrame(
                        data=chunk,
                        sample_rate=24000,
                        num_channels=1,
                        samples_per_channel=len(chunk) // 2 # Assuming 16-bit PCM
                    )
                    self._event_ch.send_nowait(
                        tts.SynthesizedAudio(frame=audio_frame)
                    )

Part 4: Orchestrating the AI CSR Agent
Finally, construct the LiveKit VoicePipelineAgent using your custom Coqui class, Faster-Whisper, and Ollama.
code Python
downloadcontent_copy
expand_less
from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli, worker
from livekit.agents.pipeline import VoicePipelineAgent
from livekit.plugins import silero, openai, faster_whisper
# Import your custom Coqui class from Part 3 here
# from my_custom_coqui import CoquiXTTS 

async def entrypoint(ctx: JobContext):
    # Connect to the LiveKit Room
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    # Instantiate the pipeline
    agent = VoicePipelineAgent(
        vad=silero.VAD.load(),
        stt=faster_whisper.STT(), # Runs locally for fast real-time transcription
        llm=openai.LLM(
            base_url="http://localhost:11434/v1", # Your Ollama local server
            api_key="ollama",
            model="llama3"
        ),
        tts=CoquiXTTS(), # <-- Your Custom Coqui Integration
        allow_interruptions=True, # Allows the caller to interrupt Coqui mid-sentence
    )

    # Start the agent and greet the phone caller
    agent.start(ctx.room)
    await agent.say("Hi, thank you for calling support. How can I help you today?", allow_interruptions=True)

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
Next Steps for You:
1. Spin up your GPU server and run docker compose up -d in the livekit/sip repo.
2. Clone coqui-ai/TTS, install it, and launch the streaming API.
3. Configure your SIP Provider (Twilio) Webhooks to point to your Server's Public IP (<public-ip>:5060)[3].
4. Dial your phone number! The SIP gateway converts your call to WebRTC, drops it into LiveKit, and the Python agent natively streams Whisper -> Ollama -> XTTSv2 back to your phone.
Sources help
1. github.com
2. github.com
3. livekit.io
4. github.com
* "livekit/sip" github livekit
* "coqui-ai/TTS" streaming xtts github
* "livekit" custom TTS plugin coqui xtts
