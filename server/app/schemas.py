from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class LogUpload(BaseModel):
    """日志上传请求"""
    device_id: str = Field(..., min_length=1, max_length=100)
    log_type: str = Field(..., pattern="^(ANR|JAVA_CRASH|TOMBSTONE|UNKNOWN)$")
    raw_content: str = Field(..., max_length=50000)
    
    class Config:
        json_schema_extra = {
            "example": {
                "device_id": "MOCK_PHONE_XIAOMI_14",
                "log_type": "JAVA_CRASH",
                "raw_content": "java.lang.NullPointerException..."
            }
        }

class CrashReport(BaseModel):
    """崩溃报告响应"""
    id: int
    device_id: str
    log_type: str
    fingerprint: str
    occurrence_count: int
    created_at: datetime
    stack_trace_preview: Optional[str] = None
    
    class Config:
        from_attributes = True

class DashboardStats(BaseModel):
    """看板统计"""
    total_devices: int
    total_crashes: int
    unique_crashes: int
    top_devices: list
    recent_crashes: list