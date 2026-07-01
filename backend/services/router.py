from providers.deepseek import call_deepseek, call_deepseek_stream
from providers.glm import call_glm, call_glm_stream
from providers.kimi import call_kimi, call_kimi_stream
from providers.qwen import call_qwen, call_qwen_stream


HANDLERS = {
    "deepseek": call_deepseek,
    "glm": call_glm,
    "kimi": call_kimi,
    "qwen": call_qwen,
}

STREAM_HANDLERS = {
    "deepseek": call_deepseek_stream,
    "glm": call_glm_stream,
    "kimi": call_kimi_stream,
    "qwen": call_qwen_stream,
}


def route_model(model: str, message: str):
    model = model.lower()

    handler = HANDLERS.get(model)

    if not handler:
        return {"success": False, "error": "not supported"}

    return handler(message)


def route_model_stream(model: str, messages: list):
    model = model.lower()

    handler = STREAM_HANDLERS.get(model)

    if not handler:
        from services.model_stability import FALLBACK_MESSAGE

        class _ErrorStream:
            status = "error"

            def __iter__(self):
                yield FALLBACK_MESSAGE

        return _ErrorStream()

    return handler(messages)
