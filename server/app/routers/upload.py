import hashlib
import re
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import CrashLog, DeviceStatus
from app.schemas import LogUpload

router = APIRouter(prefix="/api/v1", tags=["upload"])

# ============================================
# 简化版指纹算法（学习版）
# 核心思想：提取堆栈关键行 + MD5 哈希
# Pro 版使用闭源引擎，此处为教学实现
# ============================================

def extract_stack_trace(raw_content: str) -> str:
    """提取堆栈跟踪（简化版）"""
    # 匹配 "at com.xxx.xxx(xxx.java:123)" 格式
    pattern = r'at\s+([a-zA-Z_][\w.]+)\.([a-zA-Z_][\w$]*)\s*\(([^)]+)\)'
    matches = re.findall(pattern, raw_content)
    
    # 取前 3 层堆栈作为特征
    stack_key = []
    for i, (package, method, location) in enumerate(matches[:3]):
        stack_key.append(f"{package}.{method}")
    
    return "|".join(stack_key) if stack_key else raw_content[:200]

def generate_fingerprint(device_id: str, log_type: str, stack_trace: str) -> str:
    """生成崩溃指纹（简化版）"""
    # 组合关键特征
    key = f"{log_type}:{stack_trace}"
    # MD5 哈希
    return hashlib.md5(key.encode()).hexdigest()

@router.post("/upload")
async def upload_log(data: LogUpload, db: Session = Depends(get_db)):
    """
    接收设备上传的日志，执行简化版去重
    """
    # 1. 提取堆栈
    stack_trace = extract_stack_trace(data.raw_content)
    
    # 2. 生成指纹
    fingerprint = generate_fingerprint(data.device_id, data.log_type, stack_trace)
    
    # 3. 查询是否已存在
    existing = db.query(CrashLog).filter(
        CrashLog.fingerprint == fingerprint
    ).first()
    
    if existing:
        # 已存在，计数+1
        existing.occurrence_count += 1
        db.commit()
        return {
            "status": "deduplicated",
            "fingerprint": fingerprint,
            "occurrence_count": existing.occurrence_count,
            "message": "相同崩溃已记录，计数+1"
        }
    
    # 4. 新崩溃，创建记录
    new_crash = CrashLog(
        device_id=data.device_id,
        log_type=data.log_type,
        fingerprint=fingerprint,
        raw_content=data.raw_content[:5000],  # 限制大小
        stack_trace=stack_trace,
        occurrence_count=1
    )
    db.add(new_crash)
    
    # 5. 更新设备状态
    device = db.query(DeviceStatus).filter(
        DeviceStatus.device_id == data.device_id
    ).first()
    
    if device:
        device.total_uploads += 1
        device.last_seen = func.now()
    else:
        new_device = DeviceStatus(
            device_id=data.device_id,
            total_uploads=1
        )
        db.add(new_device)
    
    db.commit()
    
    return {
        "status": "new_crash",
        "fingerprint": fingerprint,
        "occurrence_count": 1,
        "message": "新崩溃已记录"
    }