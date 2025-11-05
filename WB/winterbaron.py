import os
import asyncio
import nest_asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

#  Налаштування
TOKEN = os.getenv("TOKEN") or "8422502818:AAE3iEbsck7e67HmJKVsHRMFvtnShFahbxQ"
GROUP_ID = int(os.getenv("GROUP_ID") or -4867326536)

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Словник для збереження відповідності повідомлень група <-> користувач
bridge = {}

# /start
@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer("Бот для тейков 💥💥 ")

#  Повідомлення від підписника

@dp.message(lambda msg: msg.chat.type == "private")
async def user_message(message: types.Message):
    caption = f"👤 {message.from_user.full_name} (@{message.from_user.username or 'без юзернейму'})"
    text = message.caption or message.text or ""

    # Перевірка типів контенту
    sent = None
    if message.text:
        sent = await bot.send_message(GROUP_ID, f"{caption}\n\n{message.text}")
    elif message.photo:
        sent = await bot.send_photo(GROUP_ID, message.photo[-1].file_id, caption=f"{caption}\n\n{text}")
    elif message.video:
        sent = await bot.send_video(GROUP_ID, message.video.file_id, caption=f"{caption}\n\n{text}")
    elif message.animation:  # GIF
        sent = await bot.send_animation(GROUP_ID, message.animation.file_id, caption=f"{caption}\n\n{text}")
    elif message.sticker:
        sent = await bot.send_sticker(GROUP_ID, message.sticker.file_id)
        await bot.send_message(GROUP_ID, caption)
    elif message.document:
        sent = await bot.send_document(GROUP_ID, message.document.file_id, caption=f"{caption}\n\n{text}")
    elif message.voice:
        sent = await bot.send_voice(GROUP_ID, message.voice.file_id, caption=f"{caption}\n\n{text}")
    elif message.video_note:
        sent = await bot.send_video_note(GROUP_ID, message.video_note.file_id)
        await bot.send_message(GROUP_ID, caption)
    else:
        await message.answer("this type doesn`t support (админу лень писать на это код)")
        return

    if sent:
        bridge[sent.message_id] = message.from_user.id

# Відповідь адміна

@dp.message(lambda msg: msg.chat.id == GROUP_ID and msg.reply_to_message)
async def group_reply(message: types.Message):
    replied_id = message.reply_to_message.message_id
    if replied_id not in bridge:
        return

    user_id = bridge[replied_id]
    text = message.caption or message.text or ""

    if message.text:
        await bot.send_message(user_id, text)
    elif message.photo:
        await bot.send_photo(user_id, message.photo[-1].file_id, caption=text)
    elif message.video:
        await bot.send_video(user_id, message.video.file_id, caption=text)
    elif message.animation:  # GIF
        await bot.send_animation(user_id, message.animation.file_id, caption=text)
    elif message.sticker:
        await bot.send_sticker(user_id, message.sticker.file_id)
    elif message.document:
        await bot.send_document(user_id, message.document.file_id, caption=text)
    elif message.voice:
        await bot.send_voice(user_id, message.voice.file_id, caption=text)
    elif message.video_note:
        await bot.send_video_note(user_id, message.video_note.file_id)
    else:
        await message.reply("❗️")


# Запуск

async def main():
    print("✅ Бот запущений")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        loop = asyncio.get_running_loop()
        if loop.is_running():
            nest_asyncio.apply()
            loop.create_task(main())
        else:
            loop.run_until_complete(main())
    except RuntimeError:
        asyncio.run(main())
