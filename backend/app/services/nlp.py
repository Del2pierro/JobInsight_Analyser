import spacy
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class NLPService:
    """
    Singleton service for spaCy NLP pipeline.
    Optimized for extraction tasks by disabling unused components.
    """
    _instance: Optional["NLPService"] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(NLPService, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
            
        logger.info("Initializing spaCy NLP pipeline...")
        try:
            # We use the medium French model for a good balance between speed and accuracy
            # Note: In a real environment, this model must be downloaded via:
            # python -m spacy download fr_core_news_md
            self.nlp = spacy.load("fr_core_news_md")
            logger.info("spaCy 'fr_core_news_md' loaded successfully.")
        except Exception as e:
            logger.warning(f"Could not load spaCy model 'fr_core_news_md': {e}. Falling back to blank model.")
            self.nlp = spacy.blank("fr")
            
        self._initialized = True

    def get_doc(self, text: str, disable_components: list[str] = ["parser", "ner"]):
        """
        Process text with optimized pipeline.
        By default, we disable parser and NER for simple tokenization/lemmatization/matching.
        """
        return self.nlp(text, disable=disable_components)

def get_nlp_service() -> NLPService:
    return NLPService()
