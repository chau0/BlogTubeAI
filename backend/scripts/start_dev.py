"""Development server startup script"""

import uvicorn
import sys
from pathlib import Path

# Add backend src to Python path
backend_root = Path(__file__).parent.parent
sys.path.insert(0, str(backend_root))

from src.web.app import create_app


def start_dev_server():
    """Start development server with hot reloading"""
    app = create_app()
    
    uvicorn.run(
        app,
        host="0.0.0.0", 
        port=8000,
        reload=True,
        reload_dirs=[str(backend_root / "src")],
        log_level="debug"
    )


if __name__ == "__main__":
    start_dev_server()