import discord
from views.language_view import View
from managers.state_manager import StateManager


class CancelView(View):
    """Представлення кнопки скасування"""

    def __init__(self, language_manager):
        self.__language_manager = language_manager

    def get_view(self, user_id):
        return self.__CancelView(self.__language_manager, user_id)

    class __CancelView(discord.ui.View):
        """Внутрішній клас для створення представлення кнопки скасування"""

        def __init__(self, language_manager, user_id):
            super().__init__(timeout=300)
            self.language_manager = language_manager
            self.user_id = user_id
            self.state_manager = StateManager.get_instance()
            self.lang = language_manager.get_user_language(user_id)

            for child in self.children:
                if hasattr(child, 'label') and child.label == "❌ Cancel":
                    child.label = "❌ Скасувати" if self.lang == 'uk' else "❌ Cancel"

        @discord.ui.button(label="❌ Cancel", style=discord.ButtonStyle.danger)
        async def cancel_button(self, interaction: discord.Interaction,
                                button: discord.ui.Button):
            user_id = str(interaction.user.id)

            current_state = self.state_manager.get_state(user_id)
            print(f"Скасування: поточний стан користувача {user_id}: {current_state}")

            self.state_manager.clear_state(user_id)

            new_state = self.state_manager.get_state(user_id)
            print(
                f"Скасування: новий стан користувача після очищення {user_id}: {new_state}"
            )

            from views.menu_view import MenuView
            menu_view = MenuView(self.language_manager)

            await interaction.response.send_message(
                self.language_manager.get_translation(user_id, 'action_cancelled'),
                ephemeral=True
            )

            await interaction.followup.send(
                self.language_manager.get_translation(user_id, 'main_menu'),
                view=menu_view.get_view(user_id)
            )

            self.stop()
