from openai import AsyncOpenAI
import traceback
from config import OPENAI_API_KEY
import httpx

# Создаем HTTP клиент без прокси
http_client = httpx.AsyncClient(
    proxies=None,  # Явно отключаем прокси
    timeout=60.0   # Устанавливаем таймаут
)

# Создаем клиент OpenAI с нашим HTTP клиентом
client = AsyncOpenAI(
    api_key=OPENAI_API_KEY,
    http_client=http_client
)

async def ask_gpt(prompt: str) -> str:
    try:
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",  # Используем стабильную модель
            messages=[
                {"role": "system", "content": "Ты умный и краткий ассистент, объясняй ясно."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("GPT ERROR:\n", traceback.format_exc())
        return "Извините, произошла ошибка при обращении к GPT. Попробуйте позже." 