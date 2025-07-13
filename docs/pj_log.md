# 20250712
- create UI for non technical users to use 
- design FE + BE -> review
- plan -> review

### Phase 2.1: Project Structure & Foundation (Week 1, Days 1-2)

#### Backend Setup
1. **Create FastAPI Application Structure**
   - Create `backend/` directory with proper Python package structure
   - Set up `src/web/` module for web-specific code
   - Initialize FastAPI app with CORS middleware for development
   - Configure environment variable loading for web context
   - Set up SQLite database for job tracking and history

2. **Database Schema Implementation**
   - Create migration scripts for job tracking tables
   - Implement SQLAlchemy models for jobs and job progress
   - Set up database connection and session management
   - Create initial database seeding for testing

3. **Job Management System**
   - Design in-memory job queue with UUID-based job IDs
   - Implement background task processing with asyncio
   - Create job status tracking (pending, processing, completed, failed)
   - Set up cleanup mechanisms for completed jobs

#### Frontend Setup
1. **React Project Initialization**
   - Create frontend directory with Vite + React + TypeScript template
   - Configure Tailwind CSS with custom design tokens
   - Set up shadcn/ui component library with theme configuration
   - Configure path aliases (@/) for clean imports

2. **Development Environment**
   - Set up Vite proxy configuration for API and WebSocket connections
   - Configure hot module replacement for efficient development
   - Set up TypeScript strict mode with proper tsconfig
   - Install and configure ESLint and Prettier

3. **Base Application Structure**
   - Create router setup with React Router DOM
   - Implement base layout components (Header, Sidebar, Footer)
   - Set up global state management with React Query
   - Create error boundary components for graceful error handling
