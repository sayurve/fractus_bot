import traceback
from openai import AsyncOpenAI
from config import OPENAI_API_KEY

async def ask_gpt(prompt: str) -> str:
    try:
        # Создаем клиент для каждого запроса
        client = AsyncOpenAI(api_key=OPENAI_API_KEY)
        
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
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        # Закрываем клиент после использования
        await client.close()
        
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("GPT ERROR:", traceback.format_exc())  # Полный стек ошибки
        return "Извините, произошла ошибка при обработке вашего запроса. Попробуйте позже." 