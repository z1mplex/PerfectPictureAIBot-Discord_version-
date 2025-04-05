import json
from typing import Dict, Any


class FeedbackManager:
    """Менеджер відгуків"""

    def __init__(self, feedback_file='feedback.json'):
        self.__feedback_file = feedback_file
        self.__user_feedback: Dict[str, Dict[str, Any]] = {}

    def save_feedback(self, feedback_data):
        with open(self.__feedback_file, 'a', encoding='utf-8') as file:
            json.dump(feedback_data, file, ensure_ascii=False)
            file.write('\n')

    def add_feedback_data(self, user_id, key, value):
        if str(user_id) not in self.__user_feedback:
            self.__user_feedback[str(user_id)] = {}
        self.__user_feedback[str(user_id)][key] = value

    def get_feedback_data(self, user_id):
        return self.__user_feedback.get(str(user_id), {})

    def complete_feedback(self, user_id):
        if str(user_id) in self.__user_feedback:
            self.save_feedback(self.__user_feedback[str(user_id)])
            del self.__user_feedback[str(user_id)]
