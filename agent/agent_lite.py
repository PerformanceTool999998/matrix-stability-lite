#!/usr/bin/env python3
"""
MatrixStability Lite - Agent
简化版日志采集与上传客户端
"""

import requests
import time
import hashlib
import random
from datetime import datetime

# ============================================
# 配置
# ============================================
SERVER_URL = "http://localhost:8000/api/v1"
DEVICE_ID = "DEMO_DEVICE_001"  # 学习版固定设备，实际使用可修改

# 模拟崩溃日志模板（学习版用模拟数据，实际可接入 ADB）
SAMPLE_LOGS = [
    {
        "type": "JAVA_CRASH",
        "content": """java.lang.NullPointerException: Attempt to invoke virtual method 'void android.widget.TextView.setText(java.lang.CharSequence)' on a null object reference
        at com.example.app.MainActivity.onCreate(MainActivity.java:45)
        at android.app.Activity.performCreate(Activity.java:8000)
        at android.app.Instrumentation.callActivityOnCreate(Instrumentation.java:1329)
        """
    },
    {
        "type": "ANR",
        "content": """ANR in com.example.app (com.example.app/.MainActivity)
        PID: 12345
        Reason: Input dispatching timed out
        Load: 15.2 / 12.1 / 8.5
        CPU usage from 0ms to 6000ms later:
        95% 12345/com.example.app: 85% user + 10% kernel
        """
    },
    {
        "type": "TOMBSTONE",
        "content": """*** *** *** *** *** *** *** *** *** *** *** *** *** *** *** ***
Build fingerprint: 'xiaomi/cetus/cetus:12/SKQ1.211006.001/V13.0.10.0'
Revision: '0'
ABI: 'arm64'
Timestamp: 2024-07-18 10:00:00+0800
signal 11 (SIGSEGV), code 1 (SEGV_MAPERR), fault addr 0x0
Cause: null pointer dereference
    r0  00000000  r1  00000001  r2  00000000
backtrace:
      #00 pc 000000000004a2b4  /system/lib64/libc.so (strlen+16)
      #01 pc 0000000000003f8c  /data/app/com.example.app/lib/arm64/libnative.so
        """
    }
]

def upload_log(device_id: str, log_type: str, content: str) -> dict:
    """上传日志到服务端"""
    payload = {
        "device_id": device_id,
        "log_type": log_type,
        "raw_content": content
    }
    
    try:
        response = requests.post(f"{SERVER_URL}/upload", json=payload, timeout=10)
        return response.json()
    except Exception as e:
        print(f"❌ 上传失败: {e}")
        return {"status": "error", "message": str(e)}

def simulate_device_run():
    """模拟设备运行并上传日志（学习版）"""
    print(f"🚀 MatrixStability Lite Agent 启动")
    print(f"📱 设备: {DEVICE_ID}")
    print(f"🌐 服务端: {SERVER_URL}")
    print("-" * 50)
    
    iteration = 0
    while True:
        iteration += 1
        print(f"\n⏱️  第 {iteration} 轮采集...")
        
        # 随机选择一个日志模板（模拟不同崩溃）
        log = random.choice(SAMPLE_LOGS)
        
        # 添加一些随机变化，模拟不同场景
        content = log["content"] + f"\n# 随机ID: {hashlib.md5(str(time.time()).encode()).hexdigest()[:8]}"
        
        # 上传
        result = upload_log(DEVICE_ID, log["type"], content)
        
        status_icon = "✅" if result.get("status") != "error" else "❌"
        print(f"{status_icon} 类型: {log['type']}")
        print(f"   状态: {result.get('status', 'unknown')}")
        print(f"   指纹: {result.get('fingerprint', 'N/A')[:16]}...")
        print(f"   计数: {result.get('occurrence_count', 0)}")
        print(f"   信息: {result.get('message', '')}")
        
        # 每 30 秒采集一次（学习版加速，实际可改为 5 分钟）
        time.sleep(30)

if __name__ == "__main__":
    simulate_device_run()