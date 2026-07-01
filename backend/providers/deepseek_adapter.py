from providers.deepseek import call_deepseek


class DeepSeekAdapter:

    def __init__(self):
        self.model_name = "deepseek"

    async def stream(self, prompt: str, request_id: str):

        # 调用 provider（同步版本先用）
        data = call_deepseek(prompt)

        # 统一解析
        content = (
            data.get("data")
            or data.get("choices", [{}])[0]
            .get("message", {})
            .get("content", "")
        )

        # 🔥 不用 StreamChunk，直接用 dict
        yield {
            "model": self.model_name,
            "content": content,
            "delta": content,
            "done": True,
            "request_id": request_id,
            "meta": {
                "raw": data
            }
        }