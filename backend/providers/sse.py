import json


def iter_openai_sse(response):
    for line in response.iter_lines():
        if not line:
            continue

        decoded = line.decode("utf-8")

        if not decoded.startswith("data:"):
            continue

        payload = decoded[5:].strip()

        if payload == "[DONE]":
            break

        try:
            data = json.loads(payload)
        except json.JSONDecodeError:
            continue

        content = (
            data.get("choices", [{}])[0]
            .get("delta", {})
            .get("content", "")
        )

        if content:
            yield content
