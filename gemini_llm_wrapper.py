from langchain.llms.base import LLM
from langchain.schema import Generation
from dotenv import load_dotenv
import os
import google.generativeai as genai

# Custom LangChain-compatible wrapper for Google Gemini LLM
class GeminiLLM(LLM):
    # Required property to specify the LLM type for LangChain integration
    @property
    def _llm_type(self) -> str:
        return "google-gemini"
    
    # Constructor to initialize the Gemini model
    def __init__(self, model_name="gemini-1.5-pro"):
        super().__init__()
        load_dotenv()
        # Configure the Google Gemini API with your API key from the environment
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        object.__setattr__(self, "model", genai.GenerativeModel(model_name))
    # Required method for LangChain: sends a prompt to the model and returns the result
    def _call(self, prompt: str, stop=None, run_manager=None) -> str:
        response = self.model.generate_content(prompt)
        return response.text.strip()

    def generate(self, prompts, stop=None):
        return [[Generation(text=self._call(prompt))] for prompt in prompts]

 