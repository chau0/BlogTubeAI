"""WebSocket endpoint handlers"""
import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from typing import Optional

from .manager import websocket_manager

websocket_router = APIRouter()

def get_job_manager():
    """Lazy import to avoid circular dependency"""
    from ...core.job_manager import JobManager
    return JobManager()

@websocket_router.websocket("/jobs/{job_id}")
async def websocket_job_updates(websocket: WebSocket, job_id: str):
    """WebSocket endpoint for job status updates"""
    
    job_manager = get_job_manager()
    job = await job_manager.get_job(job_id)

    if not job:
        await websocket.close(code=4004, reason="Job not found")
        return
    
    connection_id = None
    try:
        # Connect and register for updates
        connection_id = await websocket_manager.connect(websocket, job_id)
        
        # Listen for messages
        while True:
            try:
                message = await websocket.receive_text()
                await websocket_manager.handle_message(connection_id, message)
            except WebSocketDisconnect:
                break
            
    except Exception as e:
        # Log error and close connection
        print(f"WebSocket error: {e}")
        
    finally:
        # Clean up connection
        if connection_id:
            await websocket_manager.disconnect(connection_id)


@websocket_router.websocket("/system")
async def websocket_system_updates(websocket: WebSocket):
    """WebSocket endpoint for system-wide updates"""
    await websocket.accept()
    job_manager = get_job_manager()
    
    try:
        # Send system stats periodically
        while True:
            stats = {
                "type": "system_stats",
                "data": {
                    "active_jobs": job_manager.get_active_job_count(),
                    "can_accept_jobs": job_manager.can_accept_new_job(),
                    "websocket_stats": websocket_manager.get_connection_stats()
                }
            }
            
            await websocket.send_json(stats)
            await asyncio.sleep(30)  # Update every 30 seconds
            
    except WebSocketDisconnect:
        pass
    except Exception as e:
        print(f"System WebSocket error: {e}")
