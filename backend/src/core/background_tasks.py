"""Background task processing for job execution"""

import asyncio
import sys
import os
from pathlib import Path
from typing import Optional

# Add the project root to Python path so we can import existing modules
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from ..models.enums import JobStatus, JobStep
from ..services.video_service import VideoService
from ..services.provider_service import ProviderService
from .file_manager import FileManager

from ..core.youtube_parser import get_video_id, get_video_title
from ..core.transcript_handler import list_transcript_languages, fetch_transcript
from ..core.llm_providers import LLMProviderFactory
from ..core.blog_formatter import format_as_blog, save_blog_to_file
from ..core.utils import validate_url, create_safe_filename


class BackgroundTaskProcessor:
    """Processes jobs in the background using existing CLI modules"""
    
    def __init__(self, job_manager):
        self.job_manager = job_manager
        self.video_service = VideoService()
        self.provider_service = ProviderService()
        self.file_manager = FileManager()
        
        # Initialize existing CLI modules
        self.youtube_parser = YouTubeParser()
        self.transcript_handler = TranscriptHandler()
        self.llm_factory = LLMProviderFactory()
        self.blog_formatter = BlogFormatter()
    
    async def process_job(self, job_id: str) -> None:
        """Process a complete job workflow"""
        try:
            job = await self.job_manager.get_job(job_id)
            if not job:
                return
            
            # Update started time
            job.started_at = job.updated_at
            
            # Step 1: Validate URL and extract video info
            await self._update_progress(job_id, JobStep.VALIDATE_URL, "Validating YouTube URL...")
            video_info = await self._validate_and_extract_video_info(job.video_url)
            
            # Update job with video info
            job.video_id = video_info["video_id"]
            job.video_title = video_info.get("title")
            job.video_duration = video_info.get("duration")
            job.video_thumbnail = video_info.get("thumbnail")
            
            # Step 2: Detect available languages
            await self._update_progress(job_id, JobStep.DETECT_LANGUAGES, "Detecting available languages...")
            available_languages = await self._detect_languages(job.video_id)
            
            # Step 3: Fetch transcript
            await self._update_progress(job_id, JobStep.FETCH_TRANSCRIPT, "Fetching video transcript...")
            transcript = await self._fetch_transcript(job.video_id, job.language_code)
            
            # Save transcript
            transcript_path = await self.file_manager.save_transcript(job_id, transcript)
            job.transcript_file_path = transcript_path
            
            # Step 4: Generate blog content
            await self._update_progress(job_id, JobStep.GENERATE_CONTENT, "Generating blog content...")
            blog_content = await self._generate_blog_content(
                transcript, job.llm_provider, job.llm_model, job.video_title
            )
            
            # Step 5: Format and save output
            await self._update_progress(job_id, JobStep.FORMAT_BLOG, "Formatting blog post...")
            formatted_content = await self._format_blog_content(blog_content, job.video_title)
            
            # Step 6: Save final output
            await self._update_progress(job_id, JobStep.SAVE_OUTPUT, "Saving output file...")
            output_path = await self.file_manager.save_blog_output(job_id, formatted_content)
            job.output_file_path = output_path
            
            # Job completed successfully
            await self.job_manager.update_job_status(job_id, JobStatus.COMPLETED)
            
        except asyncio.CancelledError:
            await self.job_manager.update_job_status(job_id, JobStatus.CANCELLED)
            raise
        except Exception as e:
            error_message = f"Job failed: {str(e)}"
            await self.job_manager.update_job_status(job_id, JobStatus.FAILED, error_message)
            raise
    
    async def _update_progress(self, job_id: str, step: JobStep, message: str) -> None:
        """Update job progress and notify clients"""
        # This would update progress in database and notify via WebSocket
        await self.job_manager.notification_service.broadcast_progress_update(job_id, {
            "step": step.value,
            "message": message,
            "timestamp": job.updated_at.isoformat()
        })
    
    async def _validate_and_extract_video_info(self, video_url: str) -> dict:
        """Validate URL and extract video information"""
        # Use existing youtube_parser module
        loop = asyncio.get_event_loop()
        video_info = await loop.run_in_executor(
            None, self.youtube_parser.parse_url, video_url
        )
        return video_info
    
    async def _detect_languages(self, video_id: str) -> list:
        """Detect available transcript languages"""
        loop = asyncio.get_event_loop()
        languages = await loop.run_in_executor(
            None, self.transcript_handler.get_available_languages, video_id
        )
        return languages
    
    async def _fetch_transcript(self, video_id: str, language_code: str) -> str:
        """Fetch video transcript"""
        loop = asyncio.get_event_loop()
        transcript = await loop.run_in_executor(
            None, self.transcript_handler.get_transcript, video_id, language_code
        )
        return transcript
    
    async def _generate_blog_content(self, transcript: str, provider: str, 
                                   model: Optional[str], title: str) -> str:
        """Generate blog content using LLM"""
        # Use existing LLM provider
        llm_provider = self.llm_factory.get_provider(provider, model)
        
        loop = asyncio.get_event_loop()
        blog_content = await loop.run_in_executor(
            None, llm_provider.generate_blog_post, transcript, title
        )
        return blog_content
    
    async def _format_blog_content(self, content: str, title: str) -> str:
        """Format blog content"""
        loop = asyncio.get_event_loop()
        formatted_content = await loop.run_in_executor(
            None, self.blog_formatter.format_blog, content, title
        )
        return formatted_content