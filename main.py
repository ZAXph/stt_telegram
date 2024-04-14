from other import is_stt_block_limit_user, is_stt_block_limit, bot, table, stt


@bot.message_handler(commands=["start"])
def start_bot(message):
    bot.send_message(chat_id=message.chat.id,
                     text="Привет! Доступна команда:\n/stt - После написания команды, отправь боту голосовое сообщение и он его превратит в текст.")


@bot.message_handler(commands=["stt"])
def expectation_text(message):
    result = table.get_data("user_id", message.from_user.id)
    if (message.from_user.id,) not in result:
        table.add_data(message.from_user.id)
        print("Добавление в базу данных")
    elif is_stt_block_limit_user(message):
        print("У пользователя закончились Блоки")
        return
    bot.send_message(chat_id=message.chat.id, text="Отправь своё голосовое сообщение")
    bot.register_next_step_handler(message, processing_voice)


def processing_voice(message):
    if not message.voice:
        bot.send_message(chat_id=message.chat.id,
                         text="Вы отправили не голосовое сообщение! Отправьте голосовое сообщение:")
        bot.register_next_step_handler(message, processing_voice)
    else:
        amount_blocks = is_stt_block_limit(message, message.voice.duration)
        if amount_blocks is None:
            msg = bot.send_message(chat_id=message.chat.id, text="Поменяйте голосовое сообщение:")
            bot.register_next_step_handler(msg, processing_voice)
        else:  # получаем id голосового сообщения
            file_info = bot.get_file(message.voice.file_id)  # получаем информацию о голосовом сообщении
            file = bot.download_file(file_info.file_path)  # скачиваем голосовое сообщение
            success, text = stt.speech_to_text(file)
            if success:
                blocks = table.get_data("blocks", message.from_user.id)[0][0]
                table.update_data(message.from_user.id, "blocks", int(blocks) + amount_blocks)
                bot.reply_to(message, text=text)
                bot.send_message(chat_id=message.chat.id, text="Новый запрос: /stt")
            else:
                print("Возникла ошибка с SST")
                bot.send_message(chat_id=message.chat.id, text=text)


if __name__ == "__main__":
    table.create_table()
    bot.polling()
