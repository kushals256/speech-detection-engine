import sys
import os
sys.path.append(os.path.join(os.getcwd(), "backend"))

from stt_engine import STTEngine
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_stt_loading():
    logger.info("Attempting to load STT Engine...")
    try:
        engine = STTEngine(model_size="tiny", device="cpu", compute_type="int8")
        logger.info("STT Engine loaded successfully!")
    except Exception as e:
        logger.error(f"Failed to load STT Engine: {e}")
        raise

if __name__ == "__main__":
    test_stt_loading()
