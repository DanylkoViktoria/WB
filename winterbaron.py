import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import CommandStart

# 🔑 Змінні середовища (Railway або локально)
TOKEN = os.getenv("TOKEN") or "8422502818:AAE3iEbsck7e67HmJKVsHRMFvtnShFahbxQ"
GROUP_ID = int(os.getenv("GROUP_ID") or -4867326536)

# Словник для збереження відповідності повідомлень групи <-> користувач
bridge = {}

bot = Bot(token=TOKEN)
dp = Dispatcher()

# 📌 Команда /start
@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Бот для тейков💥💥")

# Користувач пише в бот
@dp.message(lambda msg: msg.chat.type == "private")
async def user_message(message: Message):
    sent = await bot.send_message(
        GROUP_ID,
        f" {message.from_user.full_name} \n{message.text}"
    )
    # Прив’язуємо повідомлення у групі до користувача
    bridge[sent.message_id] = message.from_user.id
    #await message.answer("✅ Повідомлення переслано адміну")

# Адмін відповідає у групі на повідомлення користувача
@dp.message(lambda msg: msg.chat.id == GROUP_ID and msg.reply_to_message)
async def group_reply(message: Message):
    replied_id = message.reply_to_message.message_id
    if replied_id in bridge:
        user_id = bridge[replied_id]
        await bot.send_message(
            user_id,
            f"{message.text}"
        )
    #else:
        #await message.reply("⚠ Не знайдено користувача для цієї відповіді.")

# Запуск
async def main():
    await dp.start_polling(bot)

# Spyder запуск
if __name__ == "__main__":
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        import nest_asyncio
        nest_asyncio.apply()
        asyncio.create_task(main())
    else:
        asyncio.run(main())
