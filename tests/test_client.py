import asyncio
import websockets
import numpy as np
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_client():
    uri = "ws://localhost:8000/ws/dictate"
    async with websockets.connect(uri) as websocket:
        logger.info("Connected to WebSocket")
        
        # Generate 1 second of silence/noise (16kHz, mono, int16)
        # Using random noise might trigger some output or just silence
        sample_rate = 16000
        duration = 1.0
        audio_data = np.random.randint(-100, 100, int(sample_rate * duration), dtype=np.int16)
        
        logger.info(f"Sending {len(audio_data)} bytes of audio data")
        await websocket.send(audio_data.tobytes())
        
        try:
            response = await asyncio.wait_for(websocket.recv(), timeout=10.0)
            data = json.loads(response)
            logger.info(f"Received response: {data}")
        except asyncio.TimeoutError:
            logger.warning("No response received (might be due to VAD or silence)")
        except Exception as e:
            logger.error(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_client())
