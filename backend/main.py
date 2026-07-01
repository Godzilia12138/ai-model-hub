from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from database import Base, engine
from models import Session, Message  # ⭐必须导入模型
from services.router import route_model
from api.websocket import router as ws_router
from api.session import router as session_router


load_dotenv()

app = FastAPI(title="AI Model Hub", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(session_router)
# ======================
# 启动日志
# ======================
print("MAIN LOADED")


# ======================
# 初始化数据库（关键）
# ======================
def init_db():
    try:
        Base.metadata.create_all(bind=engine)
        print("DB TABLES CREATED SUCCESSFULLY")
    except Exception as e:
        print("DB INIT ERROR:", e)


init_db()


# ======================
# HTTP 请求模型
# ======================
class ChatRequest(BaseModel):
    model: str
    message: str


# ======================
# 注册 WebSocket 路由
# ======================
app.include_router(ws_router)

print("WS ROUTER LOADED")


# ======================
# HTTP接口（单模型测试用）
# ======================
@app.post("/chat")
def chat(req: ChatRequest):
    try:
        result = route_model(req.model, req.message)
        return JSONResponse(content={
            "success": True,
            "data": result
        })
    except Exception as e:
        return JSONResponse(content={
            "success": False,
            "error": str(e)
        })


# ======================
# 健康检查
# ======================
@app.get("/")
def home():
    return {
        "message": "AI Model Hub is running",
        "status": "ok"
    }