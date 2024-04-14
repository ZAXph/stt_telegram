import requests
from config import *


class STT:
    def __init__(self):
        self.IAM_TOKEN = IAM_TOKEN
        self.FOLDER_ID = FOLDER_ID

    def speech_to_text(self, data):
        # Указываем параметры запроса
        params = "&".join([
            "topic=general",  # используем основную версию модели
            f"folderId={self.FOLDER_ID}",
            "lang=ru-RU"  # распознаём голосовое сообщение на русском языке
        ])

        # Аутентификация через IAM-токен
        headers = {
            'Authorization': f'Bearer {self.IAM_TOKEN}',
        }

        # Выполняем запрос
        response = requests.post(
            f"https://stt.api.cloud.yandex.net/speech/v1/stt:recognize?{params}",
            headers=headers,
            data=data
        )

        # Читаем json в словарь
        decoded_data = response.json()
        # Проверяем, не произошла ли ошибка при запросе
        if decoded_data.get("error_code") is None and decoded_data.get("result"):
            return True, decoded_data.get("result")  # Возвращаем статус и текст из аудио
        else:
            return False, "При запросе в SpeechKit возникла ошибка. Возможно вы отправили пустое сообщение"
