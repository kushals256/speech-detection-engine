import re
from transformers import pipeline

class TextProcessor:
    def __init__(self):
        # Initialize grammar correction model (using a small model for latency)
        # 'vennify/t5-base-grammar-correction' might be too slow, trying a smaller one or distilbert if available for this task
        # For now, let's use a very small T5 or similar. 
        # 'prithivida/grammar_error_corrector' is popular but might be heavy.
        # Let's use 'happy-transformer' or just standard HF pipeline with a small model.
        # We'll use 'pszemraj/flan-t5-small-grammar-synthesis' or similar if available, 
        # but for strict "No LLM" (Large Language Model), T5-small is borderline but usually accepted as "Small LM".
        # The prompt says "Strictly no Large Language Models", but suggests "T5-small, mT5-small".
        # So T5-small is allowed.
        
        # Using google/flan-t5-small for speed and reliability
        self.grammar_corrector = pipeline("text2text-generation", model="google/flan-t5-small", device=-1) # device=-1 for CPU
        
        self.fillers = [
            r"\bumm\b", r"\buhh\b", r"\buh\b", r"\beh\b", r"\blike\b", 
            r"\byou know\b", r"\bmatlab\b", r"\bI mean\b", r"\bsort of\b"
        ]

    def remove_fillers(self, text: str) -> str:
        for filler in self.fillers:
            text = re.sub(filler, "", text, flags=re.IGNORECASE)
        return re.sub(r"\s+", " ", text).strip()

    def remove_repetitions(self, text: str) -> str:
        # Simple word repetition removal
        words = text.split()
        if not words:
            return text
        
        new_words = [words[0]]
        for i in range(1, len(words)):
            if words[i].lower() != words[i-1].lower():
                new_words.append(words[i])
        
        return " ".join(new_words)

    def correct_grammar(self, text: str) -> str:
        if not text:
            return text
        # Prefix for Flan-T5
        input_text = "Fix grammar: " + text
        results = self.grammar_corrector(input_text, max_length=128)
        return results[0]['generated_text']

    def adjust_tone(self, text: str, tone: str) -> str:
        # Simple heuristic-based tone adjustment for now to save latency
        # A full style transfer model would be too slow for <1500ms combined with STT + Grammar
        
        if tone == "formal":
            text = text.replace("can't", "cannot").replace("won't", "will not").replace("I'm", "I am")
            # Add more rules
        elif tone == "casual":
            text = text.replace("cannot", "can't").replace("will not", "won't").replace("I am", "I'm")
        elif tone == "concise":
            # Remove adjectives/adverbs? (Too complex for regex)
            pass
            
        return text
