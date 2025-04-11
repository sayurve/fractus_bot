from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.dispatcher.filters import Command
from config import BOT_TOKEN, OPENAI_API_KEY
import openai
import asyncio

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Инициализация OpenAI
openai.api_key = OPENAI_API_KEY

@dp.message_handler(commands=["start"])
async def start_cmd(message: types.Message):
    await message.reply("Привет! Я — FRACTUS, твой безопасный финансовый ассистент 💼\n\nИспользуй команду /ask чтобы задать мне вопрос!")

@dp.message_handler(Command("ask"))
async def ask_cmd(message: types.Message):
    # Получаем текст после команды /ask
    question = message.get_args()
    if not question:
        await message.reply("Пожалуйста, добавьте ваш вопрос после команды /ask\nНапример: /ask Как вести учет расходов?")
        return

    try:
        # Отправляем индикатор набора текста
        await bot.send_chat_action(message.chat.id, "typing")
        
        # Делаем запрос к OpenAI
        completion = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты — FRACTUS, умный финансовый ассистент. Ты помогаешь пользователям с вопросами о финансах, инвестициях и управлении деньгами. Отвечай кратко и по делу."},
                {"role": "user", "content": question}
            ]
        )
        
        # Получаем ответ
        answer = completion.choices[0].message.content
        
        # Отправляем ответ пользователю
        await message.reply(answer)
        
    except Exception as e:
        await message.reply("Извините, произошла ошибка при обработке вашего запроса. Попробуйте позже.")
        print(f"Error in ask_cmd: {e}")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True) 