from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional
import os
from ..services.downloader import YouTubeDownloader

router = APIRouter(prefix="/api/downloads", tags=["downloads"])

# Request models
class DownloadRequest(BaseModel):
    url: str
    format: str = "mp3"  # mp3 or mp4
    filename: Optional[str] = None

class VideoInfoRequest(BaseModel):
    url: str

# Initialize downloader
downloader = YouTubeDownloader()

@router.post("/info")
async def get_video_info(request: VideoInfoRequest):
    """Get video information without downloading"""
    try:
        info = downloader.get_video_info(request.url)
        return {"success": True, "info": info}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error getting video info: {str(e)}")

@router.post("/download")
async def download_video(request: DownloadRequest):
    """Download video or audio"""
    try:
        if request.format.lower() == "mp3":
            result = downloader.download_audio(request.url, request.filename)
        elif request.format.lower() == "mp4":
            result = downloader.download_video(request.url, request.filename)
        else:
            raise HTTPException(status_code=400, detail="Format must be 'mp3' or 'mp4'")
        
        return {
            "success": True,
            "message": "Download completed successfully",
            "result": result
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Download failed: {str(e)}")

@router.get("/files")
async def list_downloaded_files():
    """List all downloaded files"""
    try:
        downloads_dir = "downloads"
        if not os.path.exists(downloads_dir):
            return {"files": []}
        
        files = []
        for filename in os.listdir(downloads_dir):
            if filename.endswith(('.mp3', '.mp4')):
                file_path = os.path.join(downloads_dir, filename)
                file_size = os.path.getsize(file_path)
                files.append({
                    "filename": filename,
                    "size": file_size,
                    "size_mb": round(file_size / (1024 * 1024), 2)
                })
        
        return {"files": files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing files: {str(e)}")