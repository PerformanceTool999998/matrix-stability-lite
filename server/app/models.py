from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from app.database import Base

class CrashLog(Base):
    """崩溃日志模型"""
    __tablename__ = "crash_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String(100), index=True)
    log_type = Column(String(50))  # ANR, JAVA_CRASH, TOMBSTONE
    fingerprint = Column(String(64), index=True)  # 简化版哈希
    raw_content = Column(Text)
    stack_trace = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    occurrence_count = Column(Integer, default=1)  # 去重计数

class DeviceStatus(Base):
    """设备状态模型"""
    __tablename__ = "device_status"
    
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String(100), unique=True, index=True)
    status = Column(String(20), default="online")  # online, offline, error
    last_seen = Column(DateTime(timezone=True), server_default=func.now())
    total_uploads = Column(Integer, default=0)