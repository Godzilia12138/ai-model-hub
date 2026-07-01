from fastapi import APIRouter
from database import SessionLocal
from models import Session, Message

router = APIRouter()

@router.get("/debug/db")
def debug_db():
    db = SessionLocal()

    sessions = db.query(Session).all()
    messages = db.query(Message).all()

    return {
        "session_count": len(sessions),
        "message_count": len(messages),
        "sessions": [
            {"id": s.id, "title": s.title}
            for s in sessions
        ],
        "messages": [
            {
                "id": m.id,
                "session_id": m.session_id,
                "role": m.role,
                "model": m.model,
                "content": m.content[:50]
            }
            for m in messages[:10]
        ]
    }