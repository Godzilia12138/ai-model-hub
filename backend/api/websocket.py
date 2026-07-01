from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from services.compare_ws import compare_stream, request_stop

router = APIRouter()


@router.websocket("/ws/compare")
async def ws_compare(websocket: WebSocket):
    await websocket.accept()

    print("✅ WebSocket Connected")

    try:
        while True:
            data = await websocket.receive_json()
            msg_type = data.get("type", "chat")

            if msg_type == "stop":
                session_id = data.get("session_id")
                print(f"Stop requested for session: {session_id}")
                request_stop(session_id)
                continue

            if msg_type == "chat":
                session_id = data.get("session_id")
                message = data.get("message")

                if not message:
                    await websocket.send_json({
                        "type": "error",
                        "message": "message不能为空",
                    })
                    continue

                print(f"Session: {session_id}")
                print(f"Message: {message}")

                await compare_stream(
                    session_id=session_id,
                    message=message,
                    websocket=websocket,
                )
                continue

            await websocket.send_json({
                "type": "error",
                "message": f"未知消息类型: {msg_type}",
            })

    except WebSocketDisconnect:
        print("🔌 WebSocket 已断开")

    except Exception as e:
        print("❌ WebSocket Error:", e)

        try:
            await websocket.send_json({
                "type": "error",
                "message": str(e),
            })
        except Exception:
            pass
