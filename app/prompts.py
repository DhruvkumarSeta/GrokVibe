VIBES = {
    "pro": """Translate this to professional, concise business English. Keep it direct and actionable.

Message: {text}

Professional version:""",

    "nerdy": """Remix this with sci-fi/tech humor. Keep it clear but fun. Think Star Trek or general nerd culture.

Message: {text}

Nerdy version:""",

    "cyberpunk": """Transform this to cyberpunk style: gritty, neon-lit, street slang. Think Neuromancer or Blade Runner.

Message: {text}

Cyberpunk version:""",

    "uk_slang": """Rewrite in cheeky British pub slang. Use 'proper', 'mate', 'bollocks', etc. Keep it work-appropriate.

Message: {text}

British version:""",

    "unfiltered": """Keep the raw, honest voice. Be direct and clear, drop corporate speak.

Message: {text}

Unfiltered version:"""
}

REVERSE_PROMPT = """Translate this formal message back to raw, unfiltered language. Be direct, drop the polish.

Message: {text}

Raw version:"""

def get_prompt(text: str, vibe: str = "pro", reverse: bool = False) -> str:
    if reverse:
        return REVERSE_PROMPT.format(text=text)
    template = VIBES.get(vibe, VIBES["pro"])
    return template.format(text=text)
