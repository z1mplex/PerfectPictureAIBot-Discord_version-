import discord
from managers.state_manager import StateManager, UserState
from managers.language_manager import LanguageManager
from managers.feedback_manager import FeedbackManager
from views.language_view import LanguageSelectionView
from views.menu_view import MenuView


class CommandHandler:
    """Обробник команд"""

    _instance = None

    @classmethod
    def get_instance(cls, state_manager=None, language_manager=None, feedback_manager=None):
        if cls._instance is None:
            cls._instance = CommandHandler(state_manager, language_manager, feedback_manager)
        return cls._instance

    def __init__(self, state_manager=None, language_manager=None,
                 feedback_manager=None):
        if CommandHandler._instance is not None:
            raise Exception("This class is a singleton!")

        self.state_manager = StateManager.get_instance()
        self.language_manager = language_manager if language_manager else LanguageManager()
        self.feedback_manager = feedback_manager if feedback_manager else FeedbackManager()

        CommandHandler._instance = self

    async def setup_commands(self, bot):
        @bot.tree.command(name="start", description="Почати використання бота")
        async def start(interaction: discord.Interaction):
            await interaction.response.send_message(
                self.language_manager.get_translation(str(interaction.user.id),
                                                      'choose_language'),
                view=LanguageSelectionView(self.language_manager, open_menu_after=True).get_view()
            )

        @bot.tree.command(name="services", description="Інформація про послуги")
        async def services(interaction: discord.Interaction):
            user_id = str(interaction.user.id)
            await interaction.response.send_message(
                self.language_manager.get_translation(user_id, 'services_info'))

        @bot.tree.command(name="website", description="Посилання на наш веб-сайт")
        async def website(interaction: discord.Interaction):
            user_id = str(interaction.user.id)
            await interaction.response.send_message(
                self.language_manager.get_translation(user_id, 'website'))

        @bot.tree.command(name="apply", description="Подати заявку на фотосесію")
        async def apply(interaction: discord.Interaction):
            user_id = str(interaction.user.id)
            await interaction.response.send_message(
                self.language_manager.get_translation(user_id, 'apply_session'))

        @bot.tree.command(name="generate", description="Згенерувати зображення")
        async def generate(interaction: discord.Interaction):
            await self.handle_generate_command(interaction)

        @bot.tree.command(name="feedback", description="Залишити відгук")
        async def feedback(interaction: discord.Interaction):
            await self.handle_feedback_command(interaction)

        @bot.tree.command(name="language", description="Змінити мову")
        async def language(interaction: discord.Interaction):
            await interaction.response.send_message(
                self.language_manager.get_translation(str(interaction.user.id),
                                                      'choose_language'),
                view=LanguageSelectionView(self.language_manager, open_menu_after=False).get_view()
            )

        @bot.tree.command(name="menu", description="Показати головне меню")
        async def menu(interaction: discord.Interaction):
            user_id = str(interaction.user.id)
            await interaction.response.send_message(
                self.language_manager.get_translation(user_id, 'welcome').format(
                    name=interaction.user.display_name),
                view=MenuView(self.language_manager).get_view(user_id)
            )

    async def handle_generate_command(self, interaction):
        user_id = str(interaction.user.id)
        self.state_manager.set_state(user_id, UserState.WAITING_FOR_PROMPT)

        from views.cancel_view import CancelView
        cancel_view = CancelView(self.language_manager)

        await interaction.response.send_message(
            self.language_manager.get_translation(user_id, 'generate_image_prompt'),
            view=cancel_view.get_view(user_id)
        )

    async def handle_feedback_command(self, interaction):
        user_id = str(interaction.user.id)
        self.state_manager.set_state(user_id, UserState.WAITING_FOR_NAME)

        from views.cancel_view import CancelView
        cancel_view = CancelView(self.language_manager)

        await interaction.response.send_message(
            self.language_manager.get_translation(user_id, 'feedback_prompt'),
            view=cancel_view.get_view(user_id)
        )
