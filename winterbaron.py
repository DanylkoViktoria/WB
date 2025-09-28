from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import CommandStart
import asyncio
import nest_asyncio

nest_asyncio.apply()

# Токен бота
TOKEN = "8422502818:AAE3iEbsck7e67HmJKVsHRMFvtnShFahbxQ"

# ID групи (негативне число)
GROUP_ID = -4867326536  # замініть на свій chat_id групи

# Словник для збереження зв’язку між повідомленням у групі і користувачем
bridge = {}

bot = Bot(token=TOKEN)
dp = Dispatcher()


# /start для користувача
@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Привіт! Напишіть мені повідомлення, і я перешлю його в групу.")


#  Користувач пише боту
@dp.message(lambda msg: msg.chat.type == "private")
async def user_message(message: Message):
    # Відправляємо повідомлення в групу
    sent = await bot.send_message(
        GROUP_ID,
        f"Від {message.from_user.full_name} (id:{message.from_user.id}):\n{message.text}"
    )

    # Запам’ятовуємо відповідність: id повідомлення у групі -> id користувача
    bridge[sent.message_id] = message.from_user.id

    # Сповіщаємо користувача
    await message.answer("✅ Ваше повідомлення відправлено в групу.")


# Відповідь у групі
@dp.message(lambda msg: msg.chat.id == GROUP_ID and msg.reply_to_message)
async def group_reply(message: Message):
    # Отримуємо ID повідомлення, на яке відповіли
    replied_id = message.reply_to_message.message_id

    # Шукаємо, чи це повідомлення було від користувача
    if replied_id in bridge:
        user_id = bridge[replied_id]

        # Відправляємо відповідь назад користувачу
        await bot.send_message(
            user_id,
            f"📩 Відповідь із групи:\n{message.text}"
        )


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
