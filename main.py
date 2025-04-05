import os
from dotenv import load_dotenv
from bot import DiscordBot

if __name__ == "__main__":
    if not os.path.exists('.env'):
        print("Файл .env не знайдено. Будь ласка, створіть його з вашими токенами.")
        exit(1)

    load_dotenv()

    if not os.getenv("DISCORD_TOKEN"):
        print("Будь ласка, встановіть токен Discord у файлі .env")
        exit(1)

    if not os.getenv("VYRO_API_TOKEN"):
        print("Будь ласка, встановіть Vyro API токен у файлі .env")
        exit(1)

    try:
        bot = DiscordBot.get_instance()
        print("Запуск бота...")
        bot.run()
    except KeyboardInterrupt:
        print("Програма закрита користувачем.")
    except Exception as e:
        print(f"Сталася непередбачена помилка: {str(e)}")

    print("Програма успішно завершена.")
