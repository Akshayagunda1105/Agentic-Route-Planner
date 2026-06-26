import json

from app.services.gemini_service import GeminiService
from app.prompts.parser_prompt import PARSER_PROMPT


class ParserAgent:

    def __init__(self):
        self.gemini = GeminiService()

    def parse(self, query: str):

        prompt = PARSER_PROMPT.format(
            query=query
        )

        response = self.gemini.generate_response(
            prompt
        )

        response = response.replace(
            "```json",
            ""
        )

        response = response.replace(
            "```",
            ""
        )

        response = response.strip()

        try:

            result = json.loads(response)

            return result

        except json.JSONDecodeError:

            raise ValueError(
                "Gemini returned invalid JSON."
            )