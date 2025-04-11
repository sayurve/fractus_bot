from openai import AsyncOpenAI
import traceback
from config import OPENAI_API_KEY

# Создаем клиент OpenAI
client = AsyncOpenAI(api_key=OPENAI_API_KEY)

async def ask_gpt(prompt: str) -> str:
    try:
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",  # Используем более стабильную версию
            messages=[
                {"role": "system", "content": "Ты умный, вежливый и краткий финансовый ассистент. Отвечай понятно и полезно."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("GPT ERROR:\n", traceback.format_exc())  # Покажет ошибку в логах Render
        return "Извините, произошла ошибка при обращении к GPT. Попробуйте позже." 