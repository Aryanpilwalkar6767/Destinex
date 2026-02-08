import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.db_service import db_service

def clear_db_cache():
    print("🧹 Clearing database cache...")
    try:
        # Clear all cache to ensure no bad data remains
        db_service.clear_cache()
        print("✅ Cache cleared successfully!")
    except Exception as e:
        print(f"❌ Error clearing cache: {e}")

if __name__ == "__main__":
    clear_db_cache()
