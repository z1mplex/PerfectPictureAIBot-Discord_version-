from enum import Enum
from typing import Dict


class UserState(Enum):
    """Стани користувача"""
    IDLE = 0
    WAITING_FOR_PROMPT = 1
    WAITING_FOR_NAME = 2
    WAITING_FOR_EMAIL = 3
    WAITING_FOR_FEEDBACK = 4


class StateManager:
    """Менеджер стану користувача"""

    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = StateManager()
        return cls._instance

    def __init__(self):
        if StateManager._instance is not None:
            raise Exception("This class is a singleton!")
        self.__user_states = {}
        StateManager._instance = self

    def set_state(self, user_id, state):
        user_id_str = str(user_id)
        self.__user_states[user_id_str] = state
        print(f"StateManager: Встановлено стан для користувача {user_id_str}: {state}")

    def get_state(self, user_id):
        user_id_str = str(user_id)
        state = self.__user_states.get(user_id_str, UserState.IDLE)
        print(f"StateManager: Отримано стан для користувача {user_id_str}: {state}")
        return state

    def clear_state(self, user_id):
        user_id_str = str(user_id)
        if user_id_str in self.__user_states:
            previous_state = self.__user_states[user_id_str]
            del self.__user_states[user_id_str]
            print(
                f"StateManager: Очищено стан для користувача {user_id_str}. Попередній стан: {previous_state}")
        else:
            print(
                f"StateManager: Спроба очистити стан для користувача {user_id_str}, але стан вже IDLE")

        current_state = self.get_state(user_id_str)
        if current_state != UserState.IDLE:
            print(
                f"УВАГА: Стан для користувача {user_id_str} не був очищений! Поточний стан: {current_state}")
