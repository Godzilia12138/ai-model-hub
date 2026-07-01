from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DB_URL = "mysql+pymysql://root:root@127.0.0.1:3306/ai_hub"

engine = create_engine(DB_URL, echo=True)

SessionLocal = sessionmaker(bind=engine, autoflush=False)

Base = declarative_base()