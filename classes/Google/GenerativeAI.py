import google.generativeai as genai
from classes.Helper.DataCleaner import DataParser
import os


class GoogleGenerativeAI():
    _genai_key_configured = False
    _key = os.environ.get("GOOGLE_AI_STUDIO_API_KEY")

    def __new__(cls, model_name: str = 'gemini-pro'):
        if not cls._genai_key_configured:
            genai.configure(api_key=cls._key)
            cls._genai_key_configured = True
        return super(GoogleGenerativeAI, cls).__new__(cls)

    def __init__(self, model_name: str = 'gemini-pro'):
        if f"models/{model_name}" not in [model.name for model in self.available_models]:
            raise ValueError(
                f"Model name {model_name} not found in available models.")
        self.model = genai.GenerativeModel(model_name)

    def generate_content(self, prompt: str):
        response = self.model.generate_content(prompt)
        try:
            return response.text
        except Exception as e:
            raise Exception(
                f"Error occurred while generating content. Please try again: {str(e)}")

    @property
    def available_models(self):
        return [item for item in genai.list_models() if "generateContent" in item.supported_generation_methods]
