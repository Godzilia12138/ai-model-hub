import os
import requests
from dotenv import load_dotenv
from providers.prompt import build_prompt
from services.model_stability import StableStream

load_dotenv()


def call_qwen(message: str):
    url = os.getenv("QWEN_API_URL")
    api_key = os.getenv("QWEN_API_KEY")

    if not url or not api_key:
        return {
            "success": False,
            "model": "qwen",
            "data": None,
            "error": "missing env config"
        }

    prompt = build_prompt(message)
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "qwen-plus",
        "input": {
            "messages": [
                {"role": "user", "content": prompt}
            ]
        },
        "parameters": {
            "temperature": 0.7,
            "top_p": 0.8
        }
    }

    try:
        res = requests.post(url, headers=headers, json=payload, timeout=30)
        data = res.json()

        content = (
            data.get("output", {})
            .get("text", "")
        )

        if not content:
            return {
                "success": False,
                "model": "qwen",
                "data": None,
                "error": "empty response"
            }

        return {
            "success": True,
            "model": "qwen",
            "data": content,
            "error": None
        }

    except Exception as e:
        return {
            "success": False,
            "model": "qwen",
            "data": None,
            "error": str(e)
        }


def call_qwen_stream(messages: list):
    api_key = os.getenv("QWEN_API_KEY")
    url = os.getenv(
        "QWEN_STREAM_API_URL",
        "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
    )

    payload = {
        "model": "qwen-plus",
        "messages": messages,
        "stream": True,
    }

    return StableStream("qwen", url, api_key, payload)
