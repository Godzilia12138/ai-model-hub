import os
import requests
from dotenv import load_dotenv
from providers.prompt import build_prompt
from services.model_stability import StableStream

load_dotenv()


def call_deepseek(message: str):
    url = os.getenv("DEEPSEEK_API_URL")
    api_key = os.getenv("DEEPSEEK_API_KEY")

    if not url or not api_key:
        return {
            "success": False,
            "model": "deepseek",
            "data": None,
            "error": "missing env config"
        }

    prompt = build_prompt(message)
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "stream": False
    }

    try:
        res = requests.post(url, headers=headers, json=payload, timeout=30)
        data = res.json()

        content = (
            data.get("choices", [{}])[0]
            .get("message", {})
            .get("content", "")
        )

        return {
            "success": True,
            "model": "deepseek",
            "data": content,
            "error": None
        }

    except Exception as e:
        return {
            "success": False,
            "model": "deepseek",
            "data": None,
            "error": str(e)
        }


def call_deepseek_stream(messages: list):
    url = os.getenv("DEEPSEEK_API_URL")
    api_key = os.getenv("DEEPSEEK_API_KEY")

    payload = {
        "model": "deepseek-chat",
        "messages": messages,
        "stream": True,
    }

    return StableStream("deepseek", url, api_key, payload)
