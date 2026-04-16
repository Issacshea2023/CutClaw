#!/usr/bin/env python3
"""
CutClaw API 服务
快速启动: uvicorn cutclaw_api:app --reload --port 8000

部署到 Railway/Render:
1. 创建 Railway 项目
2. 上传代码或连接 GitHub
3. 设置环境变量
4. 部署
"""

import os
import sys
import asyncio
import uuid
import tempfile
import shutil
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
import aiofiles

# 添加项目路径
CUTCLAW_DIR = Path(__file__).parent
sys.path.insert(0, str(CUTCLAW_DIR))

# 导入 CutClaw 核心模块（如果可用）
try:
    # 尝试导入配置和核心模块
    import src.config as config
    from src.video.preprocess import decode_video_to_frames
    from src.video.preprocess.asr import run_asr
    CUTCLAW_AVAILABLE = True
except ImportError as e:
    CUTCLAW_AVAILABLE = False
    print(f"⚠️ CutClaw 核心模块不可用: {e}")

# ============== 配置 ==============
UPLOAD_DIR = Path("C:/Users/梁丽娟/Videos/视频采集库/CutClaw上传")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_DIR = Path("C:/Users/梁丽娟/Videos/视频采集库/CutClaw输出")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="CutClaw API", description="视频智能剪切 API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ProcessRequest(BaseModel):
    video_path: str
    instruction: str
    audio_path: str = ""
    video_type: str = "film"
    instruction_type: str = "object"

class ProcessResponse(BaseModel):
    task_id: str
    status: str
    message: str
    output_path: str = ""

# ============== API 端点 ==============

@app.get("/")
async def root():
    return {
        "name": "CutClaw API",
        "version": "1.0.0",
        "status": "running",
        "cutclaw_available": CUTCLAW_AVAILABLE,
        "docs": "/docs"
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/upload")
async def upload_video(file: UploadFile = File(...)):
    """上传视频文件"""
    # 生成唯一文件名
    ext = os.path.splitext(file.filename)[1]
    task_id = str(uuid.uuid4())[:8]
    filename = f"{task_id}_{file.filename}"
    filepath = UPLOAD_DIR / filename
    
    # 保存文件
    content = await file.read()
    async with aiofiles.open(filepath, 'wb') as f:
        await f.write(content)
    
    return {
        "task_id": task_id,
        "filename": filename,
        "path": str(filepath),
        "size": len(content)
    }

@app.post("/process", response_model=ProcessResponse)
async def process_video(
    video: str = Form(...),
    instruction: str = Form(...),
    audio: str = Form(""),
    video_type: str = Form("film"),
    instruction_type: str = Form("object")
):
    """
    处理视频
    
    参数:
    - video: 视频文件路径
    - instruction: 剪切指令，如"保留对话场景"
    - audio: 可选的音频文件路径
    - video_type: film 或 vlog
    - instruction_type: object 或 narrative
    """
    task_id = str(uuid.uuid4())[:8]
    
    # 检查视频文件
    if not os.path.exists(video):
        raise HTTPException(status_code=404, detail=f"视频文件不存在: {video}")
    
    # 构建输出目录
    video_name = os.path.splitext(os.path.basename(video))[0]
    output_dir = OUTPUT_DIR / f"{video_name}_{task_id}"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    if not CUTCLAW_AVAILABLE:
        # 如果 CutClaw 不可用，返回模拟结果
        return ProcessResponse(
            task_id=task_id,
            status="simulated",
            message="CutClaw 核心模块未安装，返回模拟结果",
            output_path=str(output_dir)
        )
    
    # TODO: 调用实际的 CutClaw 处理逻辑
    # 这里需要根据 local_run.py 的逻辑来实现
    
    return ProcessResponse(
        task_id=task_id,
        status="processing",
        message="任务已提交处理",
        output_path=str(output_dir)
    )

@app.get("/status/{task_id}")
async def get_status(task_id: str):
    """获取任务状态"""
    # TODO: 实现状态查询
    return {
        "task_id": task_id,
        "status": "unknown",
        "progress": 0
    }

@app.get("/download/{filename}")
async def download_result(filename: str):
    """下载处理结果"""
    filepath = OUTPUT_DIR / filename
    if not filepath.exists():
        raise HTTPException(status_code=404, detail="文件不存在")
    return FileResponse(filepath, filename=filename)

# ============== 启动 ==============

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)