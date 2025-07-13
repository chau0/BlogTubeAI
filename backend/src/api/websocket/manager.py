"""WebSocket connection manager"""

import asyncio
import json
from typing import Dict, Set, Optional, Any
from datetime import datetime
import uuid

from fastapi import WebSocket


class WebSocketManager:
    """Manages WebSocket connections and message broadcasting"""
    
    def __init__(self):
        # connection_id -> WebSocket
        self.active_connections: Dict[str, WebSocket] = {}
        
        # job_id -> set of connection_ids
        self.job_subscriptions: Dict[str, Set[str]] = {}
        
        # connection_id -> metadata
        self.connection_metadata: Dict[str, Dict] = {}
        
        # connection health tracking
        self.last_ping: Dict[str, datetime] = {}
        self.heartbeat_interval = 30  # seconds
    
    async def connect(self, websocket: WebSocket, job_id: str) -> str:
        """Accept WebSocket connection and register for job updates"""
        await websocket.accept()
        
        connection_id = str(uuid.uuid4())
        self.active_connections[connection_id] = websocket
        
        # Subscribe to job updates
        if job_id not in self.job_subscriptions:
            self.job_subscriptions[job_id] = set()
        self.job_subscriptions[job_id].add(connection_id)
        
        # Store connection metadata
        self.connection_metadata[connection_id] = {
            "job_id": job_id,
            "connected_at": datetime.now(),
            "client_info": websocket.client
        }
        
        self.last_ping[connection_id] = datetime.now()
        
        # Send connection confirmation
        await self.send_to_connection(connection_id, {
            "type": "connected",
            "connection_id": connection_id,
            "job_id": job_id,
            "message": "Connected to job updates"
        })
        
        return connection_id
    
    async def disconnect(self, connection_id: str) -> None:
        """Disconnect and cleanup connection"""
        if connection_id in self.active_connections:
            # Remove from job subscriptions
            metadata = self.connection_metadata.get(connection_id, {})
            job_id = metadata.get("job_id")
            
            if job_id and job_id in self.job_subscriptions:
                self.job_subscriptions[job_id].discard(connection_id)
                
                # Clean up empty job subscriptions
                if not self.job_subscriptions[job_id]:
                    del self.job_subscriptions[job_id]
            
            # Clean up connection data
            del self.active_connections[connection_id]
            self.connection_metadata.pop(connection_id, None)
            self.last_ping.pop(connection_id, None)
    
    async def send_to_connection(self, connection_id: str, message: Dict[str, Any]) -> bool:
        """Send message to specific connection"""
        if connection_id not in self.active_connections:
            return False
        
        websocket = self.active_connections[connection_id]
        try:
            await websocket.send_text(json.dumps(message))
            return True
        except Exception:
            # Connection is dead, clean it up
            await self.disconnect(connection_id)
            return False
    
    async def broadcast_to_job(self, job_id: str, message: Dict[str, Any]) -> int:
        """Broadcast message to all connections subscribed to a job"""
        if job_id not in self.job_subscriptions:
            return 0
        
        connection_ids = list(self.job_subscriptions[job_id])
        successful_sends = 0
        
        for connection_id in connection_ids:
            if await self.send_to_connection(connection_id, message):
                successful_sends += 1
        
        return successful_sends
    
    async def handle_message(self, connection_id: str, message: str) -> None:
        """Handle incoming WebSocket message"""
        try:
            data = json.loads(message)
            message_type = data.get("type")
            
            if message_type == "ping":
                self.last_ping[connection_id] = datetime.now()
                await self.send_to_connection(connection_id, {
                    "type": "pong",
                    "timestamp": datetime.now().isoformat()
                })
            
            elif message_type == "subscribe":
                # Handle job subscription changes
                new_job_id = data.get("job_id")
                if new_job_id:
                    await self._change_job_subscription(connection_id, new_job_id)
            
        except json.JSONDecodeError:
            await self.send_to_connection(connection_id, {
                "type": "error",
                "message": "Invalid JSON message format"
            })
    
    async def _change_job_subscription(self, connection_id: str, new_job_id: str) -> None:
        """Change job subscription for a connection"""
        # Remove from current subscription
        current_metadata = self.connection_metadata.get(connection_id, {})
        current_job_id = current_metadata.get("job_id")
        
        if current_job_id and current_job_id in self.job_subscriptions:
            self.job_subscriptions[current_job_id].discard(connection_id)
        
        # Add to new subscription
        if new_job_id not in self.job_subscriptions:
            self.job_subscriptions[new_job_id] = set()
        self.job_subscriptions[new_job_id].add(connection_id)
        
        # Update metadata
        if connection_id in self.connection_metadata:
            self.connection_metadata[connection_id]["job_id"] = new_job_id
    
    async def cleanup_stale_connections(self) -> int:
        """Remove connections that haven't pinged recently"""
        stale_timeout = 60  # seconds
        current_time = datetime.now()
        stale_connections = []
        
        for connection_id, last_ping_time in self.last_ping.items():
            if (current_time - last_ping_time).seconds > stale_timeout:
                stale_connections.append(connection_id)
        
        for connection_id in stale_connections:
            await self.disconnect(connection_id)
        
        return len(stale_connections)
    
    def get_connection_stats(self) -> Dict[str, Any]:
        """Get connection statistics"""
        return {
            "total_connections": len(self.active_connections),
            "active_jobs": len(self.job_subscriptions),
            "connections_by_job": {
                job_id: len(connections) 
                for job_id, connections in self.job_subscriptions.items()
            }
        }


# Global WebSocket manager instance
websocket_manager = WebSocketManager()
