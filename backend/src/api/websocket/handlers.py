from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from .manager import manager
import logging

logger = logging.getLogger(__name__)

websocket_router = APIRouter()


@websocket_router.websocket("/job/{job_id}")
async def websocket_job_updates(websocket: WebSocket, job_id: str):
    """WebSocket endpoint for job progress updates"""
    await manager.connect(websocket, job_id)
    
    try:
        # Send initial connection confirmation
        await manager.send_personal_message({
            "type": "connection",
            "message": f"Connected to job {job_id}",
            "job_id": job_id
        }, websocket)
        
        # Keep connection alive and handle incoming messages
        while True:
            data = await websocket.receive_text()
            logger.info(f"Received message for job {job_id}: {data}")
            
            # Echo message back (for testing)
            await manager.send_personal_message({
                "type": "echo",
                "message": data,
                "job_id": job_id
            }, websocket)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket, job_id)
        logger.info(f"WebSocket disconnected for job {job_id}")
    except Exception as e:
        logger.error(f"WebSocket error for job {job_id}: {e}")
        manager.disconnect(websocket, job_id)
