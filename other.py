from config import MAX_STT_DURATION, TOKEN, MAX_USER_STT_BLOCKS
from math import ceil
import telebot
from repository import DATABASE
from stt import STT

bot = telebot.TeleBot(token=TOKEN)
table = DATABASE()
stt = STT()


def is_stt_block_limit(message, duration):

    # Переводим секунды в аудиоблоки
    audio_blocks = ceil(duration / 15)
    # округляем в большую сторону
    # Функция из БД для подсчёта всех потраченных пользователем аудиоблоков
    all_blocks = table.get_data("blocks", message.from_user.id)[0][0] + audio_blocks

    # Проверяем, что аудио длится меньше 30 секунд
    if duration >= MAX_STT_DURATION:
        msg = "SpeechKit STT работает с голосовыми сообщениями меньше 30 секунд"
        bot.send_message(message.from_user.id, msg)
        return None

    # Сравниваем all_blocks с количеством доступных пользователю аудиоблоков
    if all_blocks > MAX_USER_STT_BLOCKS:
        msg = f"Превышен общий лимит SpeechKit STT {MAX_USER_STT_BLOCKS}. Использовано {all_blocks} блоков. Доступно: {MAX_USER_STT_BLOCKS - all_blocks + audio_blocks}"
        bot.send_message(message.from_user.id, msg)
        return None

    return audio_blocks


def is_stt_block_limit_user(message):
    all_blocks = table.get_data("blocks", message.from_user.id)[0][0]
    if all_blocks == MAX_USER_STT_BLOCKS:
        msg = f"Превышен общий лимит SpeechKit TTS {MAX_USER_STT_BLOCKS}. Использовано: {all_blocks} блоков. Доступно: {MAX_USER_STT_BLOCKS - all_blocks}"
        bot.send_message(message.chat.id, msg)
        return False
    return True
