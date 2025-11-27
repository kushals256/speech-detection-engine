from text_processor import TextProcessor
import logging

logger = logging.getLogger(__name__)

class DictationPipeline:
    def __init__(self):
        self.processor = TextProcessor()
        logger.info("DictationPipeline initialized")

    def process(self, text: str, tone: str = "neutral") -> str:
        if not text:
            return ""
            
        # 1. Filler removal
        text = self.processor.remove_fillers(text)
        
        # 2. Repetition removal
        text = self.processor.remove_repetitions(text)
        
        # 3. Grammar correction
        # Only apply if text is long enough to be a sentence, otherwise it might hallucinate
        # VAD helps, but still good to be safe.
        if len(text.split()) > 3:
            text = self.processor.correct_grammar(text)
        
        # 4. Tone adjustment
        text = self.processor.adjust_tone(text, tone)
        
        return text
