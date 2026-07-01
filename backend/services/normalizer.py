def extract_content(raw: dict) -> str:
    if not isinstance(raw, dict):
        return ""

    try:
        # =========================
        # 1. OpenAI / GLM / DeepSeek / Kimi
        # =========================
        if "choices" in raw:
            choices = raw.get("choices") or []
            if choices:
                return (
                    choices[0]
                    .get("message", {})
                    .get("content", "")
                ) or ""

        # =========================
        # 2. Qwen / Kimi / 其他 output 结构
        # =========================
        output = raw.get("output")

        if isinstance(output, dict):

            # 🔥 最重要：Kimi/Qwen经常在这里
            if "text" in output:
                return output["text"] or ""

            if "content" in output:
                return output["content"] or ""

            choices = output.get("choices") or []
            if choices:
                return (
                    choices[0]
                    .get("message", {})
                    .get("content", "")
                ) or ""

        # =========================
        # 3. data包裹（某些SDK）
        # =========================
        data = raw.get("data")
        if isinstance(data, dict):
            return extract_content(data)

        # =========================
        # 4. result兜底
        # =========================
        if "result" in raw:
            return raw["result"] or ""

        return ""

    except Exception:
        return ""

def normalize(model: str, raw: dict):
    try:
        content = extract_content(raw)

        if not content:
            return {
                "success": False,
                "model": model,
                "data": None,
                "error": "empty response"
            }

        return {
            "success": True,
            "model": model,
            "data": content,
            "error": None
        }

    except Exception as e:
        return {
            "success": False,
            "model": model,
            "data": None,
            "error": str(e)
        }