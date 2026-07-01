SYSTEM_PROMPT = "你是一个AI助手，请用中文简洁回答，不要多余解释。"


def build_prompt(message: str) -> str:
    return f"""{SYSTEM_PROMPT}

用户问题：
{message}
"""
