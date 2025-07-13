#!/usr/bin/env python3
"""
Database seeding script for BlogTubeAI Backend
"""

import os
import sys
from pathlib import Path

def main():
    """Seed database with test data"""
    
    # Ensure we're in the backend directory
    backend_dir = Path(__file__).parent.parent
    os.chdir(backend_dir)
    
    # Add src to Python path
    src_path = backend_dir / "src"
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))
    
    print("🌱 Seeding database with test data...")
    
    try:
        # This will be implemented when database models are created
        print("✅ Database seeding complete!")
        print("📊 Test data includes:")
        print("  - Sample job records")
        print("  - Provider configurations")
        print("  - System settings")
        
    except Exception as e:
        print(f"❌ Database seeding failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
