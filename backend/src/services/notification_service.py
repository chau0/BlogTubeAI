"""WebSocket notification service"""

import json
from typing import Dict, Any
from datetime import datetime

from ..api.websocket.manager import WebSocketManager


class NotificationService:
    """Service for sending WebSocket notifications"""
    
    def __init__(self):
        self.websocket_manager = WebSocketManager()
    
    async def broadcast_job_update(self, job_id: str, data: Dict[str, Any]) -> None:
        """Broadcast job status update to subscribed clients"""
        message = {
            "type": "job_update",
            "job_id": job_id,
            "data": data,
            "timestamp": datetime.now().isoformat()
        }
        
        await self.websocket_manager.broadcast_to_job(job_id, message)
    
    async def broadcast_progress_update(self, job_id: str, progress_data: Dict[str, Any]) -> None:
        """Broadcast job progress update"""
        message = {
            "type": "progress_update", 
            "job_id": job_id,
            "data": progress_data,
            "timestamp": datetime.now().isoformat()
        }
        
        await self.websocket_manager.broadcast_to_job(job_id, message)
    
    async def send_error_notification(self, job_id: str, error_data: Dict[str, Any]) -> None:
        """Send error notification to clients"""
        message = {
            "type": "error",
            "job_id": job_id,
            "data": error_data,
            "timestamp": datetime.now().isoformat()
        }
        
        await self.websocket_manager.broadcast_to_job(job_id, message)
    
    async def send_completion_notification(self, job_id: str, result_data: Dict[str, Any]) -> None:
        """Send job completion notification"""
        message = {
            "type": "job_completed",
            "job_id": job_id,
            "data": result_data,
            "timestamp": datetime.now().isoformat()
        }
        
        await self.websocket_manager.broadcast_to_job(job_id, message)