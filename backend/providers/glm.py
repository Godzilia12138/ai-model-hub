import os
import requests
from dotenv import load_dotenv
from providers.prompt import build_prompt
from services.model_stability import StableStream

load_dotenv()


def call_glm(message: str):
    url = os.getenv("GLM_API_URL")
    api_key = os.getenv("GLM_API_KEY")

    if not url or not api_key:
        return {
            "success": False,
            "model": "glm",
            "data": None,
            "error": "missing env config"
        }

    prompt = build_prompt(message)

    payload = {
        "model": "glm-4-flash",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.7
    }

    try:
        res = requests.post(
            url,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json=payload,
            timeout=30
        )

        data = res.json()

        content = (
            data.get("choices", [{}])[0]
            .get("message", {})
            .get("content", "")
        )

        return {
            "success": True,
            "model": "glm",
            "data": content,
            "error": None,
            "raw": data
        }

    except Exception as e:
        return {
            "success": False,
            "model": "glm",
            "data": None,
            "error": str(e)
        }


def call_glm_stream(messages: list):
    url = os.getenv("GLM_API_URL")
    api_key = os.getenv("GLM_API_KEY")

    payload = {
        "model": "glm-4-flash",
        "messages": messages,
        "temperature": 0.7,
        "stream": True,
    }

    return StableStream("glm", url, api_key, payload)
