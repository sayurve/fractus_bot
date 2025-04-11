from openai import AsyncOpenAI
from config import OPENAI_API_KEY

# Инициализация клиента OpenAI
client = AsyncOpenAI(api_key=OPENAI_API_KEY)

async def ask_gpt(prompt: str) -> str:
    try:
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "Ты — FRACTUS, умный финансовый ассистент. Помогаешь пользователям с вопросами о финансах, инвестициях и управлении деньгами. Отвечаешь кратко и по делу."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"GPT Error: {str(e)}")  # Логируем ошибку
        return "Извините, произошла ошибка при обработке вашего запроса. Попробуйте позже." 