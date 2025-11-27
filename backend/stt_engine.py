from faster_whisper import WhisperModel
import numpy as np
import io
import logging

logger = logging.getLogger(__name__)

class STTEngine:
    def __init__(self, model_size="distil-small.en", device="cpu", compute_type="int8"):
        logger.info(f"Loading Whisper model: {model_size} on {device} with {compute_type}")
        self.model = WhisperModel(model_size, device=device, compute_type=compute_type)
        logger.info("Model loaded successfully")

    def transcribe(self, audio_data: np.ndarray, beam_size=5):
        """
        Transcribe audio data (numpy array).
        Returns the transcribed text.
        """
        # faster-whisper expects float32 audio
        if audio_data.dtype != np.float32:
            audio_data = audio_data.astype(np.float32) / 32768.0

        segments, info = self.model.transcribe(
            audio_data, 
            beam_size=1, 
            language="en", 
            vad_filter=True,
            condition_on_previous_text=False
        )
        
        text = ""
        for segment in segments:
            text += segment.text + " "
        
        return text.strip()
