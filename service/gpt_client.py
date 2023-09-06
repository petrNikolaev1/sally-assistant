from typing import List, Dict

import openai

from service.models import GPTResponse


class ChatGPT:
    def __init__(self, openai_api_key: str):
        openai.api_key = openai_api_key

    async def process(self, messages: List[Dict[str, str]]) -> GPTResponse:
        response = await openai.ChatCompletion.acreate(
            model="gpt-4",
            messages=messages,
        )
        return GPTResponse(**response)
