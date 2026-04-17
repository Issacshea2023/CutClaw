#!/usr/bin/env python3
"""
CutClaw API - Minimal Version for Cloud Deployment
"""

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uuid

app = FastAPI(title="CutClaw API", description="视频智能剪切 API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "name": "CutClaw API", 
        "version": "1.0.0",
        "status": "running",
        "message": "CutClaw API is running!",
        "endpoints": ["/", "/health", "/upload", "/process"]
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/upload")
async def upload_video(file: UploadFile = File(...)):
    """上传视频文件"""
    task_id = str(uuid.uuid4())[:8]
    return {
        "task_id": task_id,
        "filename": file.filename,
        "message": "File upload endpoint ready"
    }

@app.post("/process")
async def process_video(
    video: str = Form(...),
    instruction: str = Form(...),
    audio: str = Form(""),
    video_type: str = Form("film"),
):
    """处理视频"""
    task_id = str(uuid.uuid4())[:8]
    return {
        "task_id": task_id,
        "status": "processing",
        "message": f"Processing video: {video} with instruction: {instruction}"
    }

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)