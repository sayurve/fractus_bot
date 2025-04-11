from openai import AsyncOpenAI
from config import OPENAI_API_KEY
import traceback
import asyncio

# Создаем клиент OpenAI
client = AsyncOpenAI(
    api_key=OPENAI_API_KEY,
    timeout=60.0  # Увеличиваем таймаут
)

async def ask_gpt(prompt: str) -> str:
    try:
        # Добавляем повторные попытки при ошибке
        for attempt in range(3):
            try:
                response = await client.chat.completions.create(
                    model="gpt-3.5-turbo",  # Используем более стабильную модель
                    messages=[
                        {"role": "system", "content": "Ты краткий ассистент, объясняй просто и полезно."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=500
                )
                return response.choices[0].message.content.strip()
            except Exception as retry_error:
                if attempt == 2:  # Если это последняя попытка
                    raise retry_error
                await asyncio.sleep(1)  # Ждем секунду перед повторной попыткой
                
    except Exception as e:
        print("GPT ERROR:\n", traceback.format_exc())
        return "Извините, произошла ошибка при обращении к GPT. Попробуйте позже." 