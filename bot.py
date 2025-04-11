import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
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
async def start_cmd(message: types.Message):
    try:
        await message.reply(
            "Привет! Я — FRACTUS, твой безопасный финансовый ассистент 💼\n\n"
            "Используй команду /ask чтобы задать мне вопрос о финансах, например:\n"
            "/ask Как начать вести учет расходов?"
        )
        logger.info(f"Start command handled for user {message.from_user.id}")
    except Exception as e:
        logger.error(f"Error in start_cmd: {e}")
        await message.reply("Произошла ошибка. Попробуйте позже.")

@dp.message_handler(commands=["ask"])
async def handle_ask(message: types.Message):
    try:
        # Получаем текст после команды /ask
        prompt = message.text.replace("/ask", "").strip()
        
        if not prompt:
            await message.reply(
                "✍️ Напиши вопрос после команды, например:\n"
                "`/ask Как работает криптовалюта?`"
            )
            logger.info(f"Empty ask command from user {message.from_user.id}")
            return

        # Отправляем индикатор набора текста
        await bot.send_chat_action(message.chat.id, "typing")
        thinking_msg = await message.answer("🤖 Думаю...")
        
        # Логируем запрос
        logger.info(f"User {message.from_user.id} asked: {prompt}")
        
        # Получаем ответ от GPT
        answer = await ask_gpt(prompt)
        
        # Удаляем сообщение "Думаю..."
        await thinking_msg.delete()
        
        # Логируем ответ
        logger.info(f"Answer for user {message.from_user.id}: {answer[:100]}...")
        
        # Отправляем ответ пользователю
        await message.reply(answer)
        
    except Exception as e:
        error_msg = f"Error in handle_ask: {str(e)}"
        logger.error(error_msg)
        await message.reply(
            "😔 Извините, произошла ошибка при обработке запроса.\n"
            "Попробуйте задать вопрос позже или переформулировать его."
        )

async def on_startup(dp):
    logger.info("Bot starting...")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup) 