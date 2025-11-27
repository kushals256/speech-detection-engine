from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging
import numpy as np
import time
from stt_engine import STTEngine
from pipeline import DictationPipeline

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Intelligent Dictation Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global instances
stt_engine = None
pipeline = None

@app.on_event("startup")
async def startup_event():
    global stt_engine, pipeline
    stt_engine = STTEngine(model_size="distil-small.en", device="cpu", compute_type="int8")
    pipeline = DictationPipeline()
    logger.info("Engines initialized")

@app.get("/")
async def root():
    return {"message": "Intelligent Dictation Engine is running"}

import webrtcvad

# ... (imports)

@app.websocket("/ws/dictate")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    logger.info("Client connected")
    
    vad = webrtcvad.Vad(3) # Aggressiveness mode 3
    sample_rate = 16000
    frame_duration = 30 # ms
    frame_size = int(sample_rate * frame_duration / 1000) # 480 samples
    
    # Buffer for audio accumulation
    audio_buffer = bytearray()
    speech_buffer = bytearray()
    is_speaking = False
    silence_counter = 0
    SILENCE_THRESHOLD = 10 # frames (300ms)
    
    try:
        while True:
            data = await websocket.receive_bytes()
            audio_buffer.extend(data)
            
            # Process in 30ms frames
            while len(audio_buffer) >= frame_size * 2: # 2 bytes per sample
                frame = audio_buffer[:frame_size * 2]
                audio_buffer = audio_buffer[frame_size * 2:]
                
                is_speech = vad.is_speech(frame, sample_rate)
                
                if is_speech:
                    is_speaking = True
                    silence_counter = 0
                    speech_buffer.extend(frame)
                else:
                    if is_speaking:
                        silence_counter += 1
                        speech_buffer.extend(frame)
                        
                        if silence_counter >= SILENCE_THRESHOLD:
                            # End of speech detected
                            logger.info(f"Speech segment detected: {len(speech_buffer)} bytes")
                            
                            # Convert to numpy and transcribe
                            audio_np = np.frombuffer(speech_buffer, dtype=np.int16)
                            raw_text = stt_engine.transcribe(audio_np)
                            
                            if raw_text:
                                t0 = time.time()
                                logger.info(f"Raw: {raw_text}")
                                processed_text = pipeline.process(raw_text)
                                t1 = time.time()
                                logger.info(f"Processed: {processed_text}")
                                logger.info(f"Processing Latency: {(t1-t0)*1000:.2f}ms")
                                
                                await websocket.send_json({
                                    "raw": raw_text,
                                    "processed": processed_text,
                                    "latency_ms": (t1-t0)*1000
                                })
                            
                            # Reset
                            is_speaking = False
                            speech_buffer = bytearray()
                            silence_counter = 0
                    else:
                        # Just silence, ignore or keep a small buffer for context if needed
                        pass
                        
    except WebSocketDisconnect:
        logger.info("Client disconnected")
    except Exception as e:
        logger.error(f"Error: {e}")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
