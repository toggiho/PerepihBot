import TABLE
import config
from telebot.async_telebot import AsyncTeleBot

tgbot = AsyncTeleBot(config.TG_TOKEN)

@tgbot.message_handler(commands=['start'])
async def send_welcome(message):
	await tgbot.reply_to(message, """Привет, отправь мне свой код из Дискорда💫

Используй команду /code
Пример: /code 123456""")

@tgbot.message_handler(commands=['code'])
async def send_welcome(message):
    code = message.text.replace("/code ", "")
    try:
        int(code)
    except:
        await tgbot.reply_to(message, "❌Ваш код должен быть числом!")
        return
    
    if len(code) != 6:
        await tgbot.reply_to(message, "❌Ваш код должен содержать 6 цифр!")
        return
    
    if TABLE.tempcode_check(int(code)):
        if TABLE.get_tg_by_tempcode(code):
            await tgbot.reply_to(message, "✅Вы уже привязали вашу учетную запись")
        else:
            TABLE.add_tg_id(int(code), message.chat.id)
            await tgbot.reply_to(message, "✅Ваш код принят\nВаша учетная запись Telegram успешно привязана к серверу 'Перепиховочная'🎈")
    else:
        await tgbot.reply_to(message, "❌Ваш код неверный")
    
    
@tgbot.message_handler(commands=['allow_alert'])
async def send_message(message):
    TABLE.allow_alert(message.chat.id)
    await tgbot.reply_to(message, "🛠Функция находится в разработке🛠") #Ты разрешил отправку уведомлений!💫
     
@tgbot.message_handler(commands=['deny_alert'])
async def send_message(message):
    TABLE.deny_alert(message.chat.id)
    await tgbot.reply_to(message, "🛠Функция находится в разработке🛠") #Ты запретил отправку уведомлений!💫

# @tgbot.message_handler(func=lambda message: True)
# async def echo_all(message):
#     try:
#         int(message.text)
#     except:
#         await tgbot.reply_to(message, "Ваш код должен быть числом!")
#         return
    
#     if len(message.text) != 6:
#         await tgbot.reply_to(message, "Ваш код должен содержать 6 цифр!")
#         return
    
#     if TABLE.tempcode_check(int(message.text)):
#         TABLE.add_tg_id(int(message.text), message.chat.id)
#         await tgbot.reply_to(message, "Ваш код принят")
#     else:
#         await tgbot.reply_to(message, "Ваш код неверный")
		

import asyncio
asyncio.run(tgbot.polling())
