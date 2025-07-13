#!/usr/bin/env python3
"""
Development server startup script for BlogTubeAI Backend
"""

import os
import sys
import subprocess
from pathlib import Path


def main():
    """Start the development server with proper configuration"""

    # Ensure we're in the backend directory
    backend_dir = Path(__file__).parent.parent
    os.chdir(backend_dir)

    # Add src to Python path
    src_path = backend_dir / "src"
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))

    # Set development environment variables
    os.environ.setdefault("ENVIRONMENT", "development")
    os.environ.setdefault("DEBUG", "true")
    os.environ.setdefault("LOG_LEVEL", "DEBUG")

    # Create necessary directories
    (backend_dir / "data").mkdir(exist_ok=True)
    (backend_dir / "logs").mkdir(exist_ok=True)
    (backend_dir / "uploads").mkdir(exist_ok=True)

    print("🚀 Starting BlogTubeAI Development Server...")
    print(f"📁 Working directory: {backend_dir}")
    print(f"🐍 Python path: {sys.path[0]}")
    print("🌐 Server will be available at: http://localhost:8000")
    print("📚 API documentation at: http://localhost:8000/docs")
    print("🔧 Press Ctrl+C to stop the server")
    print("-" * 50)

    try:
        # Start uvicorn with development settings
        subprocess.run(
            [
                "uvicorn",
                "src.web.app:app",
                "--host",
                "0.0.0.0",
                "--port",
                "8000",
                "--reload",
                "--reload-dir",
                "src",
                "--log-level",
                "debug",
                "--access-log",
            ],
            check=True,
        )
    except KeyboardInterrupt:
        print("\n🛑 Development server stopped")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start server: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()