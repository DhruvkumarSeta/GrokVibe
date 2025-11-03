import asyncio
from app.prompts import get_prompt
from app.grok import translate

async def test():
    prompt = get_prompt("this code is broken", "pro")
    print("Testing Grok API translation...")
    print(f"Prompt: {prompt[:100]}...\n")

    result = await translate(prompt)
    print(f"Translation: {result}")

    assert result is not None, "Translation returned None"
    assert len(result) > 0, "Translation is empty"
    print("\n✅ Test passed: Grok API returns professional translation")

asyncio.run(test())
