"""File operations and management for the web interface"""

import os
import aiofiles
from pathlib import Path
from typing import Optional
from datetime import datetime


class FileManager:
    """Manages file operations for the web interface"""
    
    def __init__(self):
        self.base_output_dir = Path("output")
        self.transcript_dir = Path("transcripts")
        self.temp_dir = Path("temp")
        
        # Ensure directories exist
        self.base_output_dir.mkdir(exist_ok=True)
        self.transcript_dir.mkdir(exist_ok=True)
        self.temp_dir.mkdir(exist_ok=True)
    
    async def save_transcript(self, job_id: str, transcript: str) -> str:
        """Save transcript to file and return path"""
        filename = f"{job_id}_transcript.txt"
        file_path = self.transcript_dir / filename
        
        async with aiofiles.open(file_path, 'w', encoding='utf-8') as f:
            await f.write(transcript)
        
        return str(file_path)
    
    async def save_blog_output(self, job_id: str, content: str) -> str:
        """Save blog output to file and return path"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{job_id}_{timestamp}.md"
        file_path = self.base_output_dir / filename
        
        async with aiofiles.open(file_path, 'w', encoding='utf-8') as f:
            await f.write(content)
        
        return str(file_path)
    
    async def read_file(self, file_path: str) -> Optional[str]:
        """Read file content"""
        try:
            async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
                return await f.read()
        except FileNotFoundError:
            return None
    
    async def delete_file(self, file_path: str) -> bool:
        """Delete a file"""
        try:
            os.remove(file_path)
            return True
        except (FileNotFoundError, OSError):
            return False
    
    async def get_file_info(self, file_path: str) -> Optional[dict]:
        """Get file information"""
        try:
            stat = os.stat(file_path)
            return {
                "size": stat.st_size,
                "created": datetime.fromtimestamp(stat.st_ctime),
                "modified": datetime.fromtimestamp(stat.st_mtime),
                "exists": True
            }
        except (FileNotFoundError, OSError):
            return None
    
    def cleanup_temp_files(self) -> int:
        """Clean up temporary files older than 24 hours"""
        cleaned = 0
        cutoff_time = datetime.now().timestamp() - (24 * 3600)
        
        for file_path in self.temp_dir.iterdir():
            if file_path.is_file() and file_path.stat().st_mtime < cutoff_time:
                try:
                    file_path.unlink()
                    cleaned += 1
                except OSError:
                    pass
        
        return cleaned