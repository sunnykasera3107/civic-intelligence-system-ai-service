from groq import Groq
import os, logging

class GroqLLM:

    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._logger.info(f"Creating provider object: groq")
        self._llm_provider = Groq(api_key=os.getenv("GROQ_API_KEY"))

    def invoke(self, messages: list) -> str:
        self._logger.info(f"Requesting llm to answer the query: {messages}")
        return self._llm_provider.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.3
        )
