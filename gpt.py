import openai
import traceback
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

async def ask_gpt(prompt: str) -> str:
    try:
        response = await openai.ChatCompletion.acreate(
            model="gpt-4",  # Замени на "gpt-3.5-turbo", если GPT-4 не доступен
            messages=[
                {"role": "system", "content": "Ты умный, вежливый и краткий ассистент. Отвечай понятно и полезно."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("GPT ERROR:\n", traceback.format_exc())  # Покажет ошибку в логах Render
        return "Извините, произошла ошибка при обращении к GPT. Попробуйте позже." 