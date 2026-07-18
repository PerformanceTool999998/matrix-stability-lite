from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.database import engine, Base
from app.routers import upload, dashboard

# 创建数据库表
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MatrixStability Lite",
    description="Android 长稳压测学习版 - 简化指纹去重与报告看板",
    version="1.0.0-lite"
)

# 注册路由
app.include_router(upload.router)
app.include_router(dashboard.router)

# 静态文件（看板 CSS/JS）
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return {
        "message": "MatrixStability Lite API",
        "docs": "/docs",
        "dashboard": "/api/v1/dashboard"
    }