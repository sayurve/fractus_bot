from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start_cmd(message: types.Message):
    await message.reply("Привет! Я — FRACTUS, твой безопасный финансовый ассистент 💼")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True) 