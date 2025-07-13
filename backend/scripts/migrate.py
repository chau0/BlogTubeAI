#!/usr/bin/env python3
"""
Database migration script for BlogTubeAI Backend
"""

import os
import sys
from pathlib import Path

def main():
    """Run database migrations"""
    
    # Ensure we're in the backend directory
    backend_dir = Path(__file__).parent.parent
    os.chdir(backend_dir)
    
    # Add src to Python path
    src_path = backend_dir / "src"
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))
    
    # Create data directory if it doesn't exist
    data_dir = backend_dir / "data"
    data_dir.mkdir(exist_ok=True)
    
    print("🗄️  Setting up database...")
    
    try:
        # Import database setup
        from src.database.connection import init_database
        from src.database.base import Base
        from sqlalchemy import create_engine
        
        # Create database engine
        database_url = os.getenv("DATABASE_URL", "sqlite:///data/app.db")
        engine = create_engine(database_url)
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        
        print("✅ Database setup complete!")
        print(f"📁 Database location: {data_dir / 'app.db'}")
        
    except ImportError as e:
        print(f"❌ Failed to import database modules: {e}")
        print("💡 Make sure dependencies are installed: pip install -r requirements/dev.txt")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Database setup failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
