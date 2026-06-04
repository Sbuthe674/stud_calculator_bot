import aiohttp

from config import GEMINI_API_KEY, GEMINI_MODEL

SYSTEM_PROMPT = """
You are a university academic assistant.

You ONLY answer questions related to:
- GPA calculation
- grades (percent, letter, numeric)
- academic performance
- university study topics

If the question is NOT related to university or academic calculations, respond exactly:
"Sorry, I can’t answer this question."

If the user asks for programming code, algorithms, or software development tasks, also refuse.

When calculating GPA or grades:
- always show percentages and numeric values
- always show step-by-step calculation
- always give final answer clearly

Do not go outside your domain under any circumstances.

Можешь отвечать на русском если от тебя это требуют. Можно отвечать на вопросы о средней текущей оценке, рубежном
контроле и всему что связано с университетом или косввенно связанно с обучением в ней
"""

class GeminiError(Exception):
    pass


async def ask_gemini(question: str) -> str:
    if not GEMINI_API_KEY:
        raise GeminiError("Gemini API key не настроен. Пожалуйста, добавьте GEMINI_API_KEY в .env.")

    if not question.strip():
        raise GeminiError("Вопрос не может быть пустым.")

    url = (
        f"https://generativelanguage.googleapis.com/v1beta/models/"
        f"{GEMINI_MODEL}:generateContent"
    )
    params = {"key": GEMINI_API_KEY}
    payload = {
        "contents": [
            {
                "parts": [{
    "text": SYSTEM_PROMPT + "\n\nUser question:\n" + question
}],
            }
        ],
        "generationConfig": {
            "temperature": 0.7,
            "topP": 0.9,
            "maxOutputTokens": 2000,
        },
    }

    timeout = aiohttp.ClientTimeout(total=30)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.post(url, params=params, json=payload) as response:
            if response.status != 200:
                text = await response.text()
                raise GeminiError(
                    f"Ошибка Gemini API: {response.status}. Ответ: {text}"
                )
            data = await response.json()

    candidates = data.get("candidates") or []
    if not candidates:
        raise GeminiError("Gemini вернул пустой ответ.")

    content = candidates[0].get("content") or {}
    parts = content.get("parts") or []
    if not parts:
        raise GeminiError("Gemini вернул пустой ответ.")

    answer = parts[0].get("text", "").strip()
    if not answer:
        raise GeminiError("Gemini вернул пустой ответ.")

    return answer
