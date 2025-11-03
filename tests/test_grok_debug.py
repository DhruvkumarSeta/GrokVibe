import asyncio
import httpx
from app.config import GROK_API_KEY, GROK_API_URL
from app.prompts import get_prompt

async def test_debug():
    prompt = get_prompt("this code is broken", "pro")
    print("Testing Grok API with debug...")
    print(f"API URL: {GROK_API_URL}")
    print(f"API Key prefix: {GROK_API_KEY[:10]}...")
    print(f"Prompt: {prompt[:100]}...\n")

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
            print(f"Status code: {response.status_code}")
            print(f"Response: {response.text}")
            response.raise_for_status()
            data = response.json()
            print(f"Translation: {data['choices'][0]['message']['content']}")
    except Exception as e:
        print(f"Error: {e}")

asyncio.run(test_debug())
