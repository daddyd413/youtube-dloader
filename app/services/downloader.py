import os
import yt_dlp
from pathlib import Path

class YouTubeDownloader:
    def __init__(self, download_dir: str = "downloads"):
        self.download_dir = Path(download_dir)
        self.download_dir.mkdir(exist_ok=True)
    
    def download_audio(self, url: str, filename: str = None):
        """Download audio as MP3"""
        ydl_opts = {
            'format': 'bestaudio/best',
            'extractaudio': True,
            'audioformat': 'mp3',
            'outtmpl': str(self.download_dir / '%(title)s.%(ext)s'),
            'noplaylist': True,
        }
        
        if filename:
            ydl_opts['outtmpl'] = str(self.download_dir / f'{filename}.%(ext)s')
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            return {
                "title": info.get('title', 'Unknown'),
                "duration": info.get('duration', 0),
                "filename": info.get('_filename', 'unknown.mp3')
            }
    
    def download_video(self, url: str, filename: str = None):
        """Download video as MP4"""
        ydl_opts = {
            'format': 'best[ext=mp4]',
            'outtmpl': str(self.download_dir / '%(title)s.%(ext)s'),
            'noplaylist': True,
        }
        
        if filename:
            ydl_opts['outtmpl'] = str(self.download_dir / f'{filename}.%(ext)s')
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            return {
                "title": info.get('title', 'Unknown'),
                "duration": info.get('duration', 0),
                "filename": info.get('_filename', 'unknown.mp4')
            }
    
    def get_video_info(self, url: str):
        """Get video information without downloading"""
        ydl_opts = {'quiet': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return {
                "title": info.get('title', 'Unknown'),
                "duration": info.get('duration', 0),
                "thumbnail": info.get('thumbnail', ''),
                "uploader": info.get('uploader', 'Unknown')
            }