from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Session(Base):
    __tablename__ = "session"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))


class Message(Base):
    __tablename__ = "message"

    id = Column(Integer, primary_key=True, index=True)

    session_id = Column(Integer, ForeignKey("session.id"))
    role = Column(String(50))      # user / assistant
    model = Column(String(50))     # glm / kimi / qwen / deepseek
    content = Column(Text)