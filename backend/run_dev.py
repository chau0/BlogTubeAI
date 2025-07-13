"""Simple development server runner"""

import sys
import os
from pathlib import Path

# Add the backend src directory to Python path
backend_dir = Path(__file__).parent
src_dir = backend_dir / "src"
project_root = backend_dir.parent

sys.path.insert(0, str(backend_dir))
sys.path.insert(0, str(src_dir))
sys.path.insert(0, str(project_root))

# Set environment variables
os.environ.setdefault("PYTHONPATH", f"{backend_dir}:{src_dir}:{project_root}")

if __name__ == "__main__":
    import uvicorn
    
    # Run the development server
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=[str(src_dir)],
        log_level="info"
    )