import logging
import os
from aiogram import Bot, Dispatcher, executor, types
import openai

# Настраиваем логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Загружаем токены из переменных окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

logger.info(f"BOT_TOKEN: {'Установлен' if BOT_TOKEN else 'НЕ установлен'}")
logger.info(f"OPENAI_API_KEY: {'Установлен' if OPENAI_API_KEY else 'НЕ установлен'}")
logger.info(f"OPENAI_API_KEY (первые 5 символов): {OPENAI_API_KEY[:5] if OPENAI_API_KEY else 'нет'}")

# Конфигурируем OpenAI
openai.api_key = OPENAI_API_KEY

# Инициализируем бота и диспетчер
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    """Обработчик команды /start"""
    await message.reply("Привет! Я — ваш финансовый ассистент. Отправьте /echo для проверки или /gpt для тестирования GPT API.")

@dp.message_handler(commands=['echo'])
async def echo_message(message: types.Message):
    """Простое эхо сообщения для проверки работы бота"""
    logger.info("Получена команда /echo")
    await message.reply("Эхо-тест работает! Бот активен.")

@dp.message_handler(commands=['gpt'])
async def test_gpt(message: types.Message):
    """Тестирование соединения с GPT"""
    logger.info("Получена команда /gpt")
    try:
        # Сначала сообщим, что начали обработку
        await message.reply("🔄 Проверяю соединение с GPT...")
        
        # Пробуем простой запрос к GPT
        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",  # Используем более доступную модель
            messages=[
                {"role": "system", "content": "Ты помощник."},
                {"role": "user", "content": "Привет! Скажи 'Привет, соединение работает!'"}
            ]
        )
        
        answer = response.choices[0].message.content
        await message.reply(f"✅ Ответ GPT: {answer}")
        
    except Exception as e:
        logger.error(f"Ошибка при обращении к GPT: {str(e)}")
        await message.reply(f"❌ Ошибка при обращении к GPT: {str(e)}")

@dp.message_handler()
async def echo(message: types.Message):
    """Эхо всех сообщений"""
    await message.answer(f"Вы сказали: {message.text}\nОтправьте /start для начала.")

if __name__ == '__main__':
    logger.info("Запуск бота...")
    executor.start_polling(dp, skip_updates=True) 