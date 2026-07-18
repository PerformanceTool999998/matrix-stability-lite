from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db, engine
from app.models import CrashLog, DeviceStatus
from app.schemas import DashboardStats

router = APIRouter(prefix="/api/v1", tags=["dashboard"])
templates = Jinja2Templates(directory="templates")

@router.get("/dashboard")
async def dashboard_page(request: Request, db: Session = Depends(get_db)):
    """HTML 看板页面"""
    stats = get_dashboard_stats(db)
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "stats": stats,
            "title": "MatrixStability Lite - 质量看板"
        }
    )

@router.get("/stats", response_model=DashboardStats)
async def get_stats(db: Session = Depends(get_db)):
    """JSON 统计数据"""
    return get_dashboard_stats(db)

def get_dashboard_stats(db: Session):
    """获取看板统计数据"""
    # 总设备数
    total_devices = db.query(DeviceStatus).count()
    
    # 总崩溃数（去重前）
    total_crashes = db.query(func.sum(CrashLog.occurrence_count)).scalar() or 0
    
    # 独立崩溃数（去重后）
    unique_crashes = db.query(CrashLog).count()
    
    # Top 5 设备（按崩溃数）
    top_devices = db.query(
        DeviceStatus.device_id,
        DeviceStatus.total_uploads
    ).order_by(DeviceStatus.total_uploads.desc()).limit(5).all()
    
    # 最近 10 条崩溃
    recent_crashes = db.query(CrashLog).order_by(
        CrashLog.created_at.desc()
    ).limit(10).all()
    
    return {
        "total_devices": total_devices,
        "total_crashes": total_crashes,
        "unique_crashes": unique_crashes,
        "top_devices": [{"device_id": d[0], "uploads": d[1]} for d in top_devices],
        "recent_crashes": [
            {
                "id": c.id,
                "device_id": c.device_id,
                "log_type": c.log_type,
                "fingerprint": c.fingerprint[:8] + "...",
                "occurrence_count": c.occurrence_count,
                "created_at": c.created_at
            }
            for c in recent_crashes
        ]
    }