import logging
from aiogram import Bot, Dispatcher, executor, types
from config import BOT_TOKEN
from gpt import ask_gpt, http_client
import signal
import sys

# Настройка логирования
logging.basicConfig(level=logging.INFO)
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
    
    thinking_msg = await message.reply("🔄 Думаю...")
    answer = await ask_gpt(prompt)
    await thinking_msg.delete()
    await message.reply(answer)

async def on_startup(dp):
    logger.info("Бот запущен")

async def on_shutdown(dp):
    logger.info("Бот останавливается...")
    await bot.close()
    await http_client.aclose()  # Закрываем HTTP клиент

def handle_stop_signals(signum, frame):
    logger.info("Получен сигнал остановки, завершаем работу...")
    executor.stop_polling()
    sys.exit(0)

if __name__ == "__main__":
    # Регистрируем обработчики сигналов
    signal.signal(signal.SIGINT, handle_stop_signals)
    signal.signal(signal.SIGTERM, handle_stop_signals)
    
    # Запускаем бота
    executor.start_polling(
        dp,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown
    ) 