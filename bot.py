import discord
import os
import asyncio
import signal
from discord.ext import commands
from dotenv import load_dotenv

from managers.language_manager import LanguageManager
from managers.feedback_manager import FeedbackManager
from managers.state_manager import StateManager
from handlers.command_handler import CommandHandler
from handlers.message_handler import MessageHandler
from utils.constants import COMMAND_PREFIX


class DiscordBot:
    """Головний клас бота"""

    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = DiscordBot()
        return cls._instance

    def __init__(self):
        if DiscordBot._instance is not None:
            raise Exception("This class is a singleton!")

        load_dotenv()

        self.__bot = commands.Bot(command_prefix=COMMAND_PREFIX,
                                  intents=discord.Intents.all())
        self.__running = False

        self.__state_manager = StateManager()
        self.__language_manager = LanguageManager()
        self.__feedback_manager = FeedbackManager()

        self.__command_handler = CommandHandler.get_instance(
            self.__state_manager,
            self.__language_manager,
            self.__feedback_manager
        )
        self.__message_handler = MessageHandler(
            self.__state_manager,
            self.__language_manager,
            self.__feedback_manager
        )

        self.__bot.setup_hook = self.__setup_hook
        self.__bot.on_ready = self.__on_ready
        self.__bot.on_message = self.__on_message

        DiscordBot._instance = self

    async def __setup_hook(self):
        await self.__command_handler.setup_commands(self.__bot)

        await self.__bot.tree.sync()
        print("Команди синхронізовано!")

    async def __on_ready(self):
        print(f"{self.__bot.user.name} підключений до Discord!")
        await self.__bot.change_presence(
            activity=discord.Game(name="AI photos | /start"))

    async def __on_message(self, message):
        if message.author == self.__bot.user:
            return

        print(f"Received message from {message.author.id}: {message.content}")

        user_id = str(message.author.id)
        state = self.__state_manager.get_state(user_id)
        print(f"User state: {state}")

        if await self.__message_handler.handle_message(message):
            print(f"Message handled by message handler")
            return

        await self.__bot.process_commands(message)

    async def start(self):
        if not os.getenv("DISCORD_TOKEN"):
            print("Помилка: Не знайдено токен Discord бота в змінних середовища.")
            return

        try:
            self.__running = True
            await self.__bot.start(os.getenv("DISCORD_TOKEN"))
        except discord.errors.LoginFailure:
            print("Помилка: Невірний токен Discord бота.")
        except Exception as e:
            print(f"Помилка запуску бота: {e}")

    async def stop(self):
        self.__running = False
        if self.__bot:
            print("Закриваємо з'єднання з Discord...")

            try:
                if hasattr(self.__bot._connection._view_store, 'values'):
                    for view in self.__bot._connection._view_store.values():
                        view.stop()
            except Exception as e:
                print(f"Помилка при зупинці views: {e}")

            await self.__bot.close()
            print("Бот успішно завершив роботу.")

    def run(self):
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            try:
                loop.run_until_complete(self.start())
            except KeyboardInterrupt:
                print("Отримано сигнал для завершення...")
            finally:
                loop.run_until_complete(self.stop())

                pending = asyncio.all_tasks(loop)
                for task in pending:
                    task.cancel()

                if pending:
                    loop.run_until_complete(
                        asyncio.gather(*pending, return_exceptions=True))

                loop.close()
        except Exception as e:
            print(f"Помилка при запуску/закритті бота: {str(e)}")
            import traceback
            traceback.print_exc()
