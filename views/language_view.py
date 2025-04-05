import discord
from abc import ABC, abstractmethod


class View(ABC):
    """Базовий клас для представлень"""

    @abstractmethod
    def get_view(self):
        pass


class LanguageSelectionView(View):
    """Представлення вибору мови"""

    def __init__(self, language_manager, open_menu_after=False):
        self.__language_manager = language_manager
        self.__open_menu_after = open_menu_after

    def get_view(self):
        return self.__LanguageView(self.__language_manager, self.__open_menu_after)

    class __LanguageView(discord.ui.View):

        def __init__(self, language_manager, open_menu_after):
            super().__init__(timeout=180)
            self.language_manager = language_manager
            self.open_menu_after = open_menu_after

        @discord.ui.button(label="Українська", style=discord.ButtonStyle.primary)
        async def ukrainian_button(self, interaction: discord.Interaction,
                                   button: discord.ui.Button):
            user_id = str(interaction.user.id)
            self.language_manager.set_user_language(user_id, 'uk')

            await interaction.response.send_message("Вибрано українську мову.", ephemeral=True)

            if self.open_menu_after:
                from views.menu_view import MenuView
                menu_view = MenuView(self.language_manager)
                await interaction.followup.send(
                    self.language_manager.get_translation(user_id, 'welcome').format(
                        name=interaction.user.display_name),
                    view=menu_view.get_view(user_id)
                )

            self.stop()

        @discord.ui.button(label="English", style=discord.ButtonStyle.secondary)
        async def english_button(self, interaction: discord.Interaction,
                                 button: discord.ui.Button):
            user_id = str(interaction.user.id)
            self.language_manager.set_user_language(user_id, 'en')

            await interaction.response.send_message("English language selected.", ephemeral=True)

            if self.open_menu_after:
                from views.menu_view import MenuView
                menu_view = MenuView(self.language_manager)
                await interaction.followup.send(
                    self.language_manager.get_translation(user_id, 'welcome').format(
                        name=interaction.user.display_name),
                    view=menu_view.get_view(user_id)
                )

            self.stop()
