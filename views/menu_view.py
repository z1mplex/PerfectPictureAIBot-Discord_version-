import discord
from views.language_view import View

from managers.state_manager import StateManager, UserState


class MenuView(View):
    """Представлення головного меню"""

    def __init__(self, language_manager):
        self.__language_manager = language_manager

    def get_view(self, user_id):
        return self.__MenuView(self.__language_manager, user_id)

    class __MenuView(discord.ui.View):
        """Внутрішній клас для створення представлення головного меню"""

        def __init__(self, language_manager, user_id):
            super().__init__(timeout=300)
            self.language_manager = language_manager
            self.user_id = user_id
            self.lang = language_manager.get_user_language(user_id)
            self.state_manager = StateManager.get_instance()

            for child in self.children:
                if hasattr(child, 'label'):
                    if child.label == "📸 Services":
                        child.label = "📸 Послуги" if self.lang == 'uk' else "📸 Services"
                    elif child.label == "🌐 Website":
                        child.label = "🌐 Веб-сайт" if self.lang == 'uk' else "🌐 Website"
                    elif child.label == "📝 Apply":
                        child.label = "📝 Подати заявку" if self.lang == 'uk' else "📝 Apply"
                    elif child.label == "🖼️ Generate Image":
                        child.label = "🖼️ Згенерувати зображення" if self.lang == 'uk' else "🖼️ Generate Image"
                    elif child.label == "📬 Feedback":
                        child.label = "📬 Відгук" if self.lang == 'uk' else "📬 Feedback"
                    elif child.label == "🔄 Change Language":
                        child.label = "🔄 Змінити мову" if self.lang == 'uk' else "🔄 Change Language"

        async def check_and_clear_state(self, interaction):
            """Перевіряє і очищає стан користувача, якщо він відрізняється від IDLE"""
            user_id = str(interaction.user.id)
            state = self.state_manager.get_state(user_id)

            if state.value != 0:  # Якщо не IDLE
                self.state_manager.clear_state(user_id)
                await interaction.response.send_message(
                    self.language_manager.get_translation(user_id, 'action_cancelled'),
                    ephemeral=True
                )
                return True
            return False

        @discord.ui.button(label="📸 Services", style=discord.ButtonStyle.primary, row=0)
        async def services_button(self, interaction: discord.Interaction,
                                  button: discord.ui.Button):
            if await self.check_and_clear_state(interaction):
                await interaction.followup.send(
                    self.language_manager.get_translation(self.user_id, 'services_info')
                )
            else:
                await interaction.response.send_message(
                    self.language_manager.get_translation(self.user_id, 'services_info')
                )

        @discord.ui.button(label="🌐 Website", style=discord.ButtonStyle.primary, row=0)
        async def website_button(self, interaction: discord.Interaction,
                                 button: discord.ui.Button):
            if await self.check_and_clear_state(interaction):
                await interaction.followup.send(
                    self.language_manager.get_translation(self.user_id, 'website')
                )
            else:
                await interaction.response.send_message(
                    self.language_manager.get_translation(self.user_id, 'website')
                )

        @discord.ui.button(label="📝 Apply", style=discord.ButtonStyle.primary, row=1)
        async def apply_button(self, interaction: discord.Interaction,
                               button: discord.ui.Button):
            if await self.check_and_clear_state(interaction):
                await interaction.followup.send(
                    self.language_manager.get_translation(self.user_id, 'apply_session')
                )
            else:
                await interaction.response.send_message(
                    self.language_manager.get_translation(self.user_id, 'apply_session')
                )

        @discord.ui.button(label="🖼️ Generate Image", style=discord.ButtonStyle.primary,
                           row=1)
        async def generate_button(self, interaction: discord.Interaction,
                                  button: discord.ui.Button):
            if await self.check_and_clear_state(interaction):
                from handlers.command_handler import CommandHandler
                handler = CommandHandler.get_instance()

                self.state_manager.set_state(self.user_id, UserState.WAITING_FOR_PROMPT)
                await interaction.followup.send(
                    self.language_manager.get_translation(self.user_id,
                                                          'generate_image_prompt')
                )
            else:
                from handlers.command_handler import CommandHandler
                handler = CommandHandler.get_instance()
                await handler.handle_generate_command(interaction)

        @discord.ui.button(label="📬 Feedback", style=discord.ButtonStyle.secondary,
                           row=2)
        async def feedback_button(self, interaction: discord.Interaction,
                                  button: discord.ui.Button):
            if await self.check_and_clear_state(interaction):
                from handlers.command_handler import CommandHandler
                handler = CommandHandler.get_instance()

                self.state_manager.set_state(self.user_id, UserState.WAITING_FOR_NAME)
                await interaction.followup.send(
                    self.language_manager.get_translation(self.user_id,
                                                          'feedback_prompt')
                )
            else:
                from handlers.command_handler import CommandHandler
                handler = CommandHandler.get_instance()
                await handler.handle_feedback_command(interaction)

        @discord.ui.button(label="🔄 Change Language",
                           style=discord.ButtonStyle.secondary, row=2)
        async def language_button(self, interaction: discord.Interaction,
                                  button: discord.ui.Button):
            if await self.check_and_clear_state(interaction):
                from views.language_view import LanguageSelectionView
                language_view = LanguageSelectionView(self.language_manager)
                await interaction.followup.send(
                    self.language_manager.get_translation(self.user_id,
                                                          'choose_language'),
                    view=language_view.get_view()
                )
            else:
                from views.language_view import LanguageSelectionView
                language_view = LanguageSelectionView(self.language_manager)
                await interaction.response.send_message(
                    self.language_manager.get_translation(self.user_id,
                                                          'choose_language'),
                    view=language_view.get_view()
                )
