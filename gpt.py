import openai
import traceback
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

async def ask_gpt(prompt: str) -> str:
    try:
        response = await openai.ChatCompletion.acreate(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Ты вежливый, лаконичный и понятный ассистент."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("GPT ERROR:", traceback.format_exc())
        return "❗ Ошибка при обращении к GPT. Попробуйте позже." 