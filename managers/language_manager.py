import json
from dataclasses import dataclass
from typing import Dict


@dataclass
class LanguageData:
    language_code: str
    translations: Dict[str, str]


class LanguageManager:
    """Менеджер мови"""

    def __init__(self, language_file='language.json'):
        self.__language_file = language_file
        self.__user_language = self.__load_language()
        self.__translations = {
            'uk': {
                'welcome': "Привіт, {name}! Виберіть опцію з меню:",
                'choose_language': "Виберіть мову / Choose your language",
                'services_info': """
                🌟 Інформація про наші послуги 🌟

                1. 📸 Професійні фотосесії:
                   - Індивідуальні та сімейні фотосесії.
                   - Весільні та урочисті фотосесії.
                   - Дитячі та новонароджені фотосесії.

                2. 🌐 Цифровий контент:
                   - Створення та редагування зображень для соціальних мереж.
                   - Дизайн банерів та рекламних матеріалів.

                3. 🖼️ Обробка та ретушування:
                   - Професійне ретушування фотографій.
                   - Виправлення кольорів та освітлення.

                4. 🎨 Графічний дизайн:
                   - Розробка логотипів та брендової атрибутики.
                   - Дизайн поліграфічних матеріалів (візитки, листівки, плакати).

                5. 📷 Оренда фотостудії:
                   - Оренда студійного обладнання та простору для зйомок.
                   - Консультації та допомога професійних фотографів.
                """,
                'website': "Відвідайте наш веб-сайт за адресою: https://linktr.ee/indigophoto",
                'apply_session': "Для подачі заявки на фотосесію, будь ласка, заповніть нашу форму за даним посиланням: https://docs.google.com/forms/d/e/1FAIpQLSenSpsNeJVz8Nmlio-27T2vzZe2JO5DrBnxzLSb-_FPdeqpPA/viewform?usp=sf_link",
                'generate_image_prompt': "Введіть, будь ласка, опис того, що хочете згенерувати.",
                'feedback_prompt': "Напишіть ваше повне ім'я.",
                'feedback_email_prompt': "Напишіть вашу електронну пошту.",
                'feedback_text_prompt': "Напишіть ваші ідеї, пропозиції або відгуки.",
                'thank_you_feedback': "Дякуємо за ваш відгук!",
                'image_gen_error': "На жаль, я поки що не вмію цього робити 😔",
                'back_to_menu': "Повертаємось до меню",
                'change_language': "Змінити мову",
                'generating_image': "Генерую зображення, це може зайняти деякий час...",
                "action_cancelled": "Попередня дія скасована. Починаємо нову.",
                "main_menu": "Головне меню:"
            },
            'en': {
                'welcome': "Hello, {name}! Choose an option from the menu:",
                'choose_language': "Виберіть мову / Choose your language",
                'services_info': """
                🌟 Information about our services 🌟

                1. 📸 Professional Photoshoots:
                   - Individual and family photoshoots.
                   - Wedding and ceremonial photoshoots.
                   - Children and newborn photoshoots.

                2. 🌐 Digital Content:
                   - Creation and editing of images for social media.
                   - Design of banners and advertising materials.

                3. 🖼️ Editing and Retouching:
                   - Professional photo retouching.
                   - Color and lighting correction.

                4. 🎨 Graphic Design:
                   - Logo and brand identity development.
                   - Design of printed materials (business cards, flyers, posters).

                5. 📷 Studio Rental:
                   - Rental of studio equipment and shooting space.
                   - Consultations and assistance from professional photographers.
                """,
                'website': "Visit our website at: https://linktr.ee/indigophoto",
                'apply_session': "To apply for a photo session, please fill out our form at: https://docs.google.com/forms/d/e/1FAIpQLSfoPcQKYRZHHCuxLDIbZwIWefg8yKezfKap97EGYAIA-NYO6A/viewform?usp=sf_link",
                'generate_image_prompt': "Please enter the description of what you want to generate.",
                'feedback_prompt': "Please enter your full name.",
                'feedback_email_prompt': "Please enter your email address.",
                'feedback_text_prompt': "Please enter your ideas, suggestions, or feedback.",
                'thank_you_feedback': "Thank you for your feedback!",
                'image_gen_error': "Unfortunately, I can't do that yet 😔",
                'back_to_menu': "Back to Menu",
                'change_language': "Change language",
                'generating_image': "Generating image, this may take a while...",
                "action_cancelled": "Previous action cancelled. Starting new one.",
                "main_menu": "Main menu:"
            }
        }

    def __load_language(self):
        try:
            with open(self.__language_file, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def save_language(self):
        with open(self.__language_file, 'w', encoding='utf-8') as file:
            json.dump(self.__user_language, file, ensure_ascii=False, indent=4)

    def get_translation(self, user_id, key):
        language = self.get_user_language(user_id)

        if language not in self.__translations or key not in self.__translations[
            language]:
            return self.__translations.get('en', {}).get(
                key,
                f"Translation missing: {key}"
            )

        return self.__translations[language][key]

    def set_user_language(self, user_id, lang):
        self.__user_language[str(user_id)] = lang
        self.save_language()

    def get_user_language(self, user_id):
        return self.__user_language.get(str(user_id), 'uk')
