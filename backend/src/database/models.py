"""SQLAlchemy database models"""

from sqlalchemy import Column, String, Integer, DateTime, Boolean, Text, JSON, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from .connection import Base


class Job(Base):
    """Job tracking table"""
    __tablename__ = "jobs"
    
    id = Column(String, primary_key=True)
    video_id = Column(String, nullable=False)
    video_url = Column(String, nullable=False)
    video_title = Column(String)
    video_duration = Column(Integer)
    video_thumbnail = Column(String)
    language_code = Column(String, nullable=False)
    language_name = Column(String)
    llm_provider = Column(String, nullable=False)
    llm_model = Column(String)
    status = Column(String, nullable=False, default='pending')
    priority = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    error_message = Column(Text)
    error_code = Column(String)
    retry_count = Column(Integer, default=0)
    max_retries = Column(Integer, default=3)
    metadata = Column(JSON)
    
    # File paths
    transcript_file_path = Column(String)
    output_file_path = Column(String)
    
    # Processing metrics
    processing_time_seconds = Column(Integer)
    transcript_length = Column(Integer)
    output_length = Column(Integer)
    tokens_used = Column(Integer)
    
    # Relationships
    progress_entries = relationship("JobProgress", back_populates="job", cascade="all, delete-orphan")


class JobProgress(Base):
    """Job progress tracking table"""
    __tablename__ = "job_progress"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    job_id = Column(String, ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False)
    step = Column(String, nullable=False)
    status = Column(String, nullable=False)
    message = Column(Text)
    progress_percentage = Column(Integer, default=0)
    details = Column(JSON)
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    error_details = Column(Text)
    
    # Relationships
    job = relationship("Job", back_populates="progress_entries")


class JobStep(Base):
    """Job step definitions table"""
    __tablename__ = "job_steps"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    step_name = Column(String, unique=True, nullable=False)
    display_name = Column(String, nullable=False)
    description = Column(Text)
    estimated_duration_seconds = Column(Integer)
    is_required = Column(Boolean, default=True)
    order_index = Column(Integer, nullable=False)
    retry_allowed = Column(Boolean, default=True)


class WebSocketConnection(Base):
    """WebSocket connection tracking table"""
    __tablename__ = "websocket_connections"
    
    id = Column(String, primary_key=True)
    job_id = Column(String, ForeignKey("jobs.id", ondelete="CASCADE"))
    client_ip = Column(String)
    user_agent = Column(String)
    connected_at = Column(DateTime, default=datetime.utcnow)
    last_ping = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)


class SystemConfig(Base):
    """System configuration table"""
    __tablename__ = "system_config"
    
    key = Column(String, primary_key=True)
    value = Column(String, nullable=False)
    value_type = Column(String, default='string')
    description = Column(Text)
    is_secret = Column(Boolean, default=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ProviderStatus(Base):
    """LLM provider status table"""
    __tablename__ = "provider_status"
    
    provider_name = Column(String, primary_key=True)
    is_available = Column(Boolean, default=True)
    last_check = Column(DateTime, default=datetime.utcnow)
    response_time_ms = Column(Integer)
    error_message = Column(Text)
    quota_remaining = Column(Integer)
    quota_reset_at = Column(DateTime)


class AuditLog(Base):
    """Audit log table"""
    __tablename__ = "audit_log"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    job_id = Column(String, ForeignKey("jobs.id"))
    action = Column(String, nullable=False)
    details = Column(JSON)
    client_ip = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)