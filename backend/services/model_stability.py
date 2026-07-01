import time
import requests
from providers.sse import iter_openai_sse

FALLBACK_MESSAGE = "模型暂不可用"
MAX_RETRIES = 2
RETRY_DELAY_SEC = 0.5
IMMEDIATE_429_MODELS = {"kimi", "qwen"}


class StableStream:
    """带重试与 429 处理的 OpenAI 兼容流式请求。"""

    def __init__(self, model_name: str, url: str, api_key: str, payload: dict):
        self.model_name = model_name
        self.url = url
        self.api_key = api_key
        self.payload = payload
        self.status = "success"

    def __iter__(self):
        yield from self._run()

    def _headers(self):
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def _fallback(self):
        self.status = "error"
        yield FALLBACK_MESSAGE

    def _run(self):
        if not self.url or not self.api_key:
            print(f"[{self.model_name}] missing env config")
            yield from self._fallback()
            return

        for attempt in range(MAX_RETRIES + 1):
            try:
                res = requests.post(
                    self.url,
                    headers=self._headers(),
                    json=self.payload,
                    stream=True,
                    timeout=60,
                )

                if res.status_code == 429:
                    print(f"[{self.model_name}] 429 rate limited (attempt {attempt + 1})")
                    if self.model_name in IMMEDIATE_429_MODELS:
                        yield from self._fallback()
                        return
                    if attempt < MAX_RETRIES:
                        time.sleep(RETRY_DELAY_SEC)
                        continue
                    yield from self._fallback()
                    return

                res.raise_for_status()

                has_content = False
                for chunk in iter_openai_sse(res):
                    has_content = True
                    yield chunk

                if has_content:
                    return

                print(f"[{self.model_name}] empty stream (attempt {attempt + 1})")

            except requests.HTTPError as e:
                code = e.response.status_code if e.response is not None else None
                print(f"[{self.model_name}] HTTP {code}: {e} (attempt {attempt + 1})")
                if code == 429 and self.model_name in IMMEDIATE_429_MODELS:
                    yield from self._fallback()
                    return

            except Exception as e:
                print(f"[{self.model_name}] error: {e} (attempt {attempt + 1})")

            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY_SEC)

        yield from self._fallback()


def make_result(model: str, data: str, status: str = "success") -> dict:
    return {
        "model": model,
        "data": data,
        "status": status,
    }
