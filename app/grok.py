import httpx
from app.config import GROK_API_KEY, GROK_API_URL

async def translate(prompt: str) -> str:
    """Call Grok API and return translated text."""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                GROK_API_URL,
                headers={
                    "Authorization": f"Bearer {GROK_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "grok-2-1212",
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 150,
                    "temperature": 0.7
                }
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"Grok API error: {e}")
        return None
