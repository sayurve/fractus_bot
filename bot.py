import logging
from aiogram import Bot, Dispatcher, executor, types
from config import BOT_TOKEN
from gpt import ask_gpt

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def handle_start(message: types.Message):
    await message.reply("Привет! Я — FRACTUS, твой безопасный финансовый ассистент 🧠\n\nИспользуй команду /ask чтобы задать мне вопрос!")

@dp.message_handler(commands=["ask"])
async def handle_ask(message: types.Message):
    prompt = message.text.replace("/ask", "").strip()
    if not prompt:
        await message.reply("Пожалуйста, добавьте ваш вопрос после команды /ask\nНапример: /ask Как вести учет расходов?")
        return
    await message.reply("🔄 Думаю...")
    answer = await ask_gpt(prompt)
    await message.reply(answer)

async def on_startup(dp):
    logger.info("Bot starting...")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup) 