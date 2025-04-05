import os
import requests
import asyncio
from abc import ABC, abstractmethod


class ImageGenerationServiceInterface(ABC):
    """Інтерфейс для сервісу генерації зображень"""

    @abstractmethod
    async def generate_image(self, prompt_text):
        pass


class VyroImageGenerationService(ImageGenerationServiceInterface):

    def __init__(self, api_token=None):
        self.__api_token = api_token or os.getenv("VYRO_API_TOKEN")
        self.__url = 'https://api.vyro.ai/v1/imagine/api/generations'

    async def generate_image(self, prompt_text):
        headers = {
            'Authorization': f'Bearer {self.__api_token}'
        }

        payload = {
            'prompt': (None, prompt_text),
            'style_id': (None, '29')
        }

        try:
            print(f"Sending request to Vyro API with prompt: {prompt_text}")
            print(f"API URL: {self.__url}")

            if not self.__api_token:
                print("Error: VYRO_API_TOKEN not found or empty")
                return None

            response = await asyncio.to_thread(
                lambda: requests.post(self.__url, headers=headers, files=payload)
            )

            print(f"API response status: {response.status_code}")
            if response.status_code != 200:
                print(f"API error response: {response.text}")

            return response
        except Exception as e:
            print(f"Помилка генерації зображення: {e}")
            return None
