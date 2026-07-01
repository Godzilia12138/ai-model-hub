from fastapi import APIRouter
from database import SessionLocal
from models import Session, Message

router = APIRouter()


@router.get("/sessions")
def get_sessions():
    db = SessionLocal()

    try:
        sessions = db.query(Session).order_by(Session.id.desc()).all()

        return [
            {"id": s.id, "title": s.title}
            for s in sessions
        ]
    finally:
        db.close()


@router.get("/messages/{session_id}")
def get_messages(session_id: int):
    db = SessionLocal()

    try:
        msgs = db.query(Message).filter(
            Message.session_id == session_id
        ).order_by(Message.id.asc()).all()

        return [
            {
                "role": m.role,
                "model": m.model,
                "content": m.content
            }
            for m in msgs
        ]
    finally:
        db.close()