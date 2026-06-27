import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

def run_llm_call(prompt: str, model: str = None) -> str:
    """
    Runs a call to the Google Gemini LLM with the specified prompt.
    
    Args:
        prompt (str): The prompt string to send to the model.
        model (str): The model name to use. Defaults to GEMINI_MODEL in .env or "gemini-2.5-flash".
        
    Returns:
        str: The generated text response from the LLM.
    """
    if model is None:
        model = os.getenv("GEMINI_MODEL", "gemini-3.1-flash-lite")

    # The client automatically picks up the GEMINI_API_KEY from the environment
    client = genai.Client()
    
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0.2,
        )
    )
    
    return response.text
