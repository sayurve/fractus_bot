import openai
import traceback
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

async def ask_gpt(prompt: str) -> str:
    try:
        response = await openai.ChatCompletion.acreate(
            model="gpt-4",  # или "gpt-3.5-turbo"
            messages=[
                {"role": "system", "content": "Ты краткий ассистент, отвечай ясно и полезно."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("GPT ERROR:\n", traceback.format_exc())
        return "Извините, произошла ошибка при обращении к GPT. Попробуйте позже." 