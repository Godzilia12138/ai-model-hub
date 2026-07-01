import asyncio
import threading
from database import SessionLocal
from models import Message
from services.router import route_model_stream
from services.history import get_or_create_session, build_model_messages
from services.model_stability import FALLBACK_MESSAGE

MODELS = ["glm", "qwen", "kimi", "deepseek"]

# session_id -> 是否停止生成
STOP_FLAGS = {}


class WsSender:
    def __init__(self, websocket):
        self.websocket = websocket
        self._lock = asyncio.Lock()

    async def send(self, data: dict):
        async with self._lock:
            await self.websocket.send_json(data)


def save_message(db, session_id, role, model, content):
    msg = Message(
        session_id=session_id,
        role=role,
        model=model,
        content=content,
    )
    db.add(msg)
    db.commit()


def request_stop(session_id):
    if session_id is not None:
        STOP_FLAGS[session_id] = True


def clear_stop(session_id):
    if session_id is not None:
        STOP_FLAGS[session_id] = False


def is_stopped(session_id, stop_flags):
    return bool(stop_flags.get(session_id))


async def stream_model(model, messages, sender: WsSender, db, session_id, stop_flags):
    buffer = ""
    status = "success"
    loop = asyncio.get_running_loop()
    chunk_queue = asyncio.Queue()
    stream = route_model_stream(model, messages)

    def produce():
        nonlocal status
        try:
            for chunk in stream:
                if is_stopped(session_id, stop_flags):
                    break
                future = asyncio.run_coroutine_threadsafe(chunk_queue.put(chunk), loop)
                future.result(timeout=120)
            if not is_stopped(session_id, stop_flags):
                status = getattr(stream, "status", "success")
        except Exception as e:
            print(f"[{model}] stream produce error: {e}")
            status = "error"
            if not is_stopped(session_id, stop_flags):
                asyncio.run_coroutine_threadsafe(
                    chunk_queue.put(FALLBACK_MESSAGE), loop
                ).result(timeout=10)
        finally:
            asyncio.run_coroutine_threadsafe(chunk_queue.put(None), loop).result(timeout=10)

    threading.Thread(target=produce, daemon=True).start()

    while True:
        if is_stopped(session_id, stop_flags):
            break

        chunk = await chunk_queue.get()
        if chunk is None:
            break

        if is_stopped(session_id, stop_flags):
            break

        buffer += chunk

        await sender.send({
            "model": model,
            "data": buffer,
            "status": "success",
            "done": False,
        })

    await sender.send({
        "model": model,
        "data": buffer,
        "status": status,
        "done": True,
    })

    if buffer:
        await asyncio.to_thread(save_message, db, session_id, "assistant", model, buffer)

    return buffer


async def compare_stream(message: str, websocket, session_id=None, stop_flags=None):
    if stop_flags is None:
        stop_flags = STOP_FLAGS

    db = SessionLocal()
    sender = WsSender(websocket)

    try:
        print("compare_stream start:", message[:50], "session_id:", session_id)

        session, is_new = get_or_create_session(db, session_id, message)
        db_session_id = session.id
        print("session:", db_session_id, "is_new:", is_new)

        clear_stop(db_session_id)

        if is_new:
            await sender.send({
                "type": "session",
                "session_id": db_session_id,
            })

        await asyncio.to_thread(
            save_message, db, db_session_id, "user", "user", message
        )

        await asyncio.gather(*[
            stream_model(
                model,
                build_model_messages(db, db_session_id, model),
                sender,
                db,
                db_session_id,
                stop_flags,
            )
            for model in MODELS
        ], return_exceptions=True)

        print("compare_stream done")

    except Exception as e:
        print("compare_stream error:", e)

    finally:
        db.close()
