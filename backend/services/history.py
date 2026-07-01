from providers.prompt import SYSTEM_PROMPT
from models import Session, Message


def get_or_create_session(db, session_id, title: str):
    if session_id:
        session = db.query(Session).filter(Session.id == session_id).first()
        if session:
            return session, False

    session = Session(title=(title or "新对话")[:20])
    db.add(session)
    db.commit()
    db.refresh(session)
    return session, True


def build_model_messages(db, session_id: int, model_name: str) -> list:
    rows = (
        db.query(Message)
        .filter(Message.session_id == session_id)
        .order_by(Message.id.asc())
        .all()
    )

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    for row in rows:
        if row.role == "user":
            messages.append({"role": "user", "content": row.content})
        elif row.role == "assistant" and row.model == model_name:
            messages.append({"role": "assistant", "content": row.content})

    return messages
