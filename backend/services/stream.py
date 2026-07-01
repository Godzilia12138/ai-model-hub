import asyncio
from providers.glm import call_glm
from providers.qwen import call_qwen
from providers.kimi import call_kimi
from providers.deepseek import call_deepseek


# =========================
# 1️⃣ 统一 safe_call（关键）
# =========================
async def safe_call(fn, message, model_name):
    try:
        res = await asyncio.to_thread(fn, message)

        if not res:
            return {"model": model_name, "data": ""}

        # 兼容不同模型返回结构
        data = (
            res.get("data")
            or res.get("result")
            or res.get("output", {}).get("text")
            or ""
        )

        return {
            "model": model_name,
            "data": data
        }

    except Exception as e:
        return {
            "model": model_name,
            "data": f"error: {str(e)}"
        }


# =========================
# 2️⃣ 流式输出函数
# =========================
async def stream_text(model, text, websocket):
    buffer = ""

    for char in text:
        buffer += char

        await websocket.send_json({
            "model": model,
            "data": buffer,
            "done": False
        })

        await asyncio.sleep(0.02)  # 更丝滑一点

    await websocket.send_json({
        "model": model,
        "data": buffer,
        "done": True
    })


# =========================
# 3️⃣ 主逻辑
# =========================
async def compare_stream(message: str, websocket):

    try:
        # 🚀 并发调用4个模型
        glm, qwen, kimi, deepseek = await asyncio.gather(
            safe_call(call_glm, message, "glm"),
            safe_call(call_qwen, message, "qwen"),
            safe_call(call_kimi, message, "kimi"),
            safe_call(call_deepseek, message, "deepseek"),
        )

        # 🔥 调试（建议保留）
        print("GLM:", glm)
        print("QWEN:", qwen)
        print("KIMI:", kimi)
        print("DEEPSEEK:", deepseek)

        # 📦 统一结构
        results = {
            glm["model"]: glm["data"],
            qwen["model"]: qwen["data"],
            kimi["model"]: kimi["data"],
            deepseek["model"]: deepseek["data"]
        }

        # ⚡ 并发流式输出
        await asyncio.gather(*[
            stream_text(model, text, websocket)
            for model, text in results.items()
        ])

    except Exception as e:
        await websocket.send_json({
            "model": "error",
            "data": str(e),
            "done": True
        })

    finally:
    
            pass