from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from config import BOT_TOKEN
from gpt import ask_gpt

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start_cmd(message: types.Message):
    await message.reply(
        "Привет! Я — FRACTUS, твой безопасный финансовый ассистент 💼\n\n"
        "Используй команду /ask чтобы задать мне вопрос о финансах, например:\n"
        "/ask Как начать вести учет расходов?"
    )

@dp.message_handler(commands=["ask"])
async def handle_ask(message: types.Message):
    # Получаем текст после команды /ask
    prompt = message.text.replace("/ask", "").strip()
    
    if not prompt:
        await message.reply(
            "✍️ Напиши вопрос после команды, например:\n"
            "`/ask Как работает криптовалюта?`"
        )
        return

    # Отправляем индикатор набора текста
    await message.answer("🤖 Думаю...")
    
    # Получаем ответ от GPT
    answer = await ask_gpt(prompt)
    
    # Отправляем ответ пользователю
    await message.reply(answer)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True) 