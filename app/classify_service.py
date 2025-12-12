from openai import AsyncOpenAI
from .config import settings

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

async def classify_article(title, summary):
    prompt = f"Classify this news article into a category: {title}\n{summary}"

    try:
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        print("Classification response:", response)
        return response.choices[0].message.content
    except Exception as e:
        print("Classification error:", e)
        return "Uncategorized"
