import os
import google.generativeai as genai
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class GeminiService:
    """
    Service to interact with Google Gemini AI.
    """
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-pro')
            logger.info("Gemini Service initialized.")
        else:
            self.model = None
            logger.warning("Gemini API Key missing. Advisor will be limited.")

    async def generate_advice(self, prompt: str) -> str:
        if not self.model:
            return "Désolé, l'assistant IA est actuellement déconnecté (Clé API manquante)."
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.error(f"Error calling Gemini: {e}")
            return "Une erreur est survenue lors de la génération de vos conseils."

def get_gemini_service() -> GeminiService:
    return GeminiService()
