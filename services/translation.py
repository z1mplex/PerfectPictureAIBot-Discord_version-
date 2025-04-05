from abc import ABC, abstractmethod
from googletrans import Translator


class TranslationServiceInterface(ABC):
    """Інтерфейс для сервісу перекладу"""

    @abstractmethod
    def translate(self, text, target_lang):
        pass


class GoogleTranslationService(TranslationServiceInterface):

    def __init__(self):
        self.__translator = Translator()

    def translate(self, text, target_lang='en'):
        try:
            translation = self.__translator.translate(text, src='auto', dest=target_lang)
            return translation.text
        except Exception as e:
            print(f"Помилка перекладу: {e}")
            return text
