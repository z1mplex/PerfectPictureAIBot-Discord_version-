"""Константи та конфігураційні змінні"""

# Префікс команд
COMMAND_PREFIX = '!'

# Таймаути (секунди)
LANGUAGE_VIEW_TIMEOUT = 180  # 3 хвилини
MENU_VIEW_TIMEOUT = 300  # 5 хвилин

# Файли
LANGUAGE_FILE = 'language.json'
FEEDBACK_FILE = 'feedback.json'

# Стилі зображень
IMAGE_STYLES = {
    'realistic': '29',
    'anime': '28',
    'fantasy': '27',
    'abstract': '26'
}

# URL API
VYRO_API_URL = 'https://api.vyro.ai/v1/imagine/api/generations'
