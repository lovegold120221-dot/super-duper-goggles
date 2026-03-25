import aiohttp
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
