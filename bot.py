import logging
from aiogram import Bot, Dispatcher, executor, types
from config import BOT_TOKEN
from gpt import ask_gpt
import signal
import sys
import traceback

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def handle_start(message: types.Message):
    try:
        logger.info(f"Получена команда /start от пользователя {message.from_user.id}")
        await message.reply(
            "Привет! Я — FRACTUS, твой безопасный финансовый ассистент 🧠\n\n"
            "Используй команду /ask чтобы задать мне вопрос!\n"
            "Например: /ask Что такое инфляция?"
        )
    except Exception as e:
        logger.error(f"Ошибка в команде /start: {traceback.format_exc()}")
        await message.reply("Произошла ошибка. Пожалуйста, попробуйте позже.")

@dp.message_handler(commands=["ask"])
async def handle_ask(message: types.Message):
    try:
        logger.info(f"Получена команда /ask от пользователя {message.from_user.id}")
        prompt = message.text.replace("/ask", "").strip()
        
        if not prompt:
            await message.reply(
                "Пожалуйста, добавьте ваш вопрос после команды /ask\n"
                "Например: /ask Как вести учет расходов?"
            )
            return
        
        thinking_msg = await message.reply("🤔 Думаю...")
        logger.info(f"Отправляем запрос к GPT: {prompt}")
        
        answer = await ask_gpt(prompt)
        await thinking_msg.delete()
        await message.reply(answer)
        
    except Exception as e:
        logger.error(f"Ошибка в команде /ask: {traceback.format_exc()}")
        await message.reply("Произошла ошибка при обработке запроса. Пожалуйста, попробуйте позже.")

async def on_startup(dp):
    try:
        logger.info("Бот запускается...")
        # Здесь можно добавить инициализацию базы данных или другие настройки
    except Exception as e:
        logger.error(f"Ошибка при запуске: {traceback.format_exc()}")

async def on_shutdown(dp):
    try:
        logger.info("Бот останавливается...")
        await bot.close()
    except Exception as e:
        logger.error(f"Ошибка при остановке: {traceback.format_exc()}")

def handle_stop_signals(signum, frame):
    logger.info("Получен сигнал остановки, завершаем работу...")
    executor.stop_polling()
    sys.exit(0)

if __name__ == "__main__":
    try:
        # Регистрируем обработчики сигналов
        signal.signal(signal.SIGINT, handle_stop_signals)
        signal.signal(signal.SIGTERM, handle_stop_signals)
        
        logger.info("Запускаем бота...")
        # Запускаем бота
        executor.start_polling(
            dp,
            skip_updates=True,
            on_startup=on_startup,
            on_shutdown=on_shutdown
        )
    except Exception as e:
        logger.error(f"Критическая ошибка: {traceback.format_exc()}")
        sys.exit(1) 