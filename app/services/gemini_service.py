import time

from google import genai

from app.config.settings import (
    GEMINI_API_KEY,
    MODEL_NAME
)


class GeminiService:

    def __init__(self):

        self.client = genai.Client(
            api_key=GEMINI_API_KEY
        )

    def generate_response(self, prompt: str) -> str:

        retries = 3

        for attempt in range(retries):

            try:

                response = self.client.models.generate_content(
                    model=MODEL_NAME,
                    contents=prompt
                )

                return response.text.strip()

            except Exception as e:

                print(
                    f"Attempt {attempt + 1} failed."
                )

                if attempt == retries - 1:

                    raise RuntimeError(
                        f"Gemini API Error: {str(e)}"
                    )

                time.sleep(2)