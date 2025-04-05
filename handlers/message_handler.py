import discord
import os
from managers.state_manager import UserState
from services.translation import GoogleTranslationService
from services.image_generation import VyroImageGenerationService


class MessageHandler:
    """Обробник повідомлень"""

    def __init__(self, state_manager, language_manager, feedback_manager):
        self.state_manager = state_manager
        self.language_manager = language_manager
        self.feedback_manager = feedback_manager
        self.translator = GoogleTranslationService()
        self.image_generator = VyroImageGenerationService()

    async def handle_message(self, message):
        user_id = str(message.author.id)
        state = self.state_manager.get_state(user_id)

        if state == UserState.IDLE:
            return False

        if state == UserState.WAITING_FOR_PROMPT:
            await self.handle_generate_image(message)
            return True
        if state == UserState.WAITING_FOR_NAME:
            await self.handle_feedback_name(message)
            return True
        if state == UserState.WAITING_FOR_EMAIL:
            await self.handle_feedback_email(message)
            return True
        if state == UserState.WAITING_FOR_FEEDBACK:
            await self.handle_feedback_text(message)
            return True

        return False

    async def handle_generate_image(self, message):
        user_id = str(message.author.id)

        translated_text = self.translator.translate(message.content, 'en')

        print(f"Original text: {message.content}")
        print(f"Translated text: {translated_text}")

        await message.channel.send(
            self.language_manager.get_translation(user_id, 'generating_image'))

        response = await self.image_generator.generate_image(translated_text)

        print(f"API response status: {response.status_code if response else 'None'}")

        if response and response.status_code == 200:
            temp_file_path = f'temp_image_{user_id}.jpg'
            with open(temp_file_path, 'wb') as f:
                f.write(response.content)

            file = discord.File(temp_file_path)
            await message.channel.send(file=file)

            os.remove(temp_file_path)
        else:
            await message.channel.send(
                self.language_manager.get_translation(user_id, 'image_gen_error'))

        self.state_manager.clear_state(user_id)

    async def handle_feedback_name(self, message):
        user_id = str(message.author.id)

        self.feedback_manager.add_feedback_data(user_id, 'full_name', message.content)
        self.state_manager.set_state(user_id, UserState.WAITING_FOR_EMAIL)

        from views.cancel_view import CancelView
        cancel_view = CancelView(self.language_manager)

        await message.channel.send(
            self.language_manager.get_translation(user_id, 'feedback_email_prompt'),
            view=cancel_view.get_view(user_id)
        )

    async def handle_feedback_email(self, message):
        user_id = str(message.author.id)

        self.feedback_manager.add_feedback_data(user_id, 'email', message.content)
        self.state_manager.set_state(user_id, UserState.WAITING_FOR_FEEDBACK)

        from views.cancel_view import CancelView
        cancel_view = CancelView(self.language_manager)

        await message.channel.send(
            self.language_manager.get_translation(user_id, 'feedback_text_prompt'),
            view=cancel_view.get_view(user_id)
        )

    async def handle_feedback_text(self, message):
        user_id = str(message.author.id)

        self.feedback_manager.add_feedback_data(user_id, 'feedback_text',
                                                message.content)
        self.feedback_manager.complete_feedback(user_id)

        await message.channel.send(
            self.language_manager.get_translation(user_id, 'thank_you_feedback'))

        self.state_manager.clear_state(user_id)
