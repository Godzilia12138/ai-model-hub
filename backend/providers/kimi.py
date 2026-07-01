import os
import requests
from dotenv import load_dotenv
from services.response import success, fail
from providers.prompt import build_prompt
from services.model_stability import StableStream

load_dotenv()


def call_kimi(message: str):
    try:
        url = os.getenv("KIMI_API_URL")
        api_key = os.getenv("KIMI_API_KEY")

        if not url or not api_key:
            return fail("kimi", "missing env config")

        prompt = build_prompt(message)

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "moonshot-v1-8k",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7
        }

        res = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=30
        )

        res.raise_for_status()

        data = res.json()

        content = (
            data.get("choices", [{}])[0]
            .get("message", {})
            .get("content", "")
        )

        if not content:
            return fail("kimi", "empty response")

        return {
            "success": True,
            "model": "kimi",
            "data": content,
            "raw": data
        }

    except Exception as e:
        return fail("kimi", str(e))


def call_kimi_stream(messages: list):
    url = os.getenv("KIMI_API_URL")
    api_key = os.getenv("KIMI_API_KEY")

    payload = {
        "model": "moonshot-v1-8k",
        "messages": messages,
        "temperature": 0.7,
        "stream": True,
    }

    return StableStream("kimi", url, api_key, payload)
