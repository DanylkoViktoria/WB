import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import CommandStart

#  Змінні середовища
TOKEN = os.getenv("TOKEN") or "8422502818:AAE3iEbsck7e67HmJKVsHRMFvtnShFahbxQ"
GROUP_ID = int(os.getenv("GROUP_ID") or -4867326536)

bridge = {}

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Бот для тейков💥💥")

@dp.message(lambda msg: msg.chat.type == "private")
async def user_message(message: Message):
    sent = await bot.send_message(
        GROUP_ID,
        f"Від {message.from_user.full_name} (id:{message.from_user.id}):\n{message.text}"
    )
    bridge[sent.message_id] = message.from_user.id
    await message.answer("✅ Сообщение отправлено")

@dp.message(lambda msg: msg.chat.id == GROUP_ID and msg.reply_to_message)
async def group_reply(message: Message):
    replied_id = message.reply_to_message.message_id
    if replied_id in bridge:
        user_id = bridge[replied_id]
        await bot.send_message(
            user_id,
            f"{message.text}"
        )

async def main():
    await dp.start_polling(bot)

# 🔹 Spyder/Jupyter-friendly запуск
if __name__ == "__main__":
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        # Якщо loop вже працює (Spyder/Jupyter)
        import nest_asyncio
        nest_asyncio.apply()      # дозволяє запускати корутини всередині вже працюючого loop
        asyncio.create_task(main())
    else:
        asyncio.run(main())
