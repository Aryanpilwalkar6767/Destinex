"""
Database Service for DESTINEX
Handles MongoDB connections and caching logic
"""

from pymongo import MongoClient
from datetime import datetime, timedelta
import os


class DatabaseService:
    """
    Service class for MongoDB operations.
    Caches city search results to reduce API calls and improve performance.
    """
    
    def __init__(self):
        """
        Initialize MongoDB connection.
        Uses local MongoDB instance (free).
        """
        # Connect to local MongoDB (make sure MongoDB is running locally)
        # Default connection: mongodb://localhost:27017/
        mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
        
        try:
            self.client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
            self.db = self.client['destinex_db']
            self.cache_collection = self.db['city_cache']
            
            # Create index on city name for faster lookups
            self.cache_collection.create_index('city_name', unique=True)
            
            print("✅ Connected to MongoDB successfully")
            
        except Exception as e:
            print(f"❌ MongoDB Connection Error: {e}")
            print("Make sure MongoDB is running locally!")
            raise
    
    def get_cached_data(self, city_name):
        """
        Retrieve cached data for a city if it exists and is not expired.
        
        Args:
            city_name (str): Name of the city to search
            
        Returns:
            dict or None: Cached data if valid, None otherwise
        """
        try:
            # Normalize city name (lowercase for consistency)
            normalized_city = city_name.lower().strip()
            
            # Find cached entry
            cached = self.cache_collection.find_one({'city_name': normalized_city})
            
            if cached:
                # Check if cache is expired (24 hours)
                cached_time = cached.get('cached_at')
                if cached_time:
                    age = datetime.utcnow() - cached_time
                    if age < timedelta(hours=24):
                        print(f"✅ Cache HIT for '{city_name}'")
                        return cached.get('data')
                    else:
                        print(f"⏰ Cache EXPIRED for '{city_name}'")
                else:
                    print(f"✅ Cache HIT for '{city_name}' (no expiry)")
                    return cached.get('data')
            
            print(f"❌ Cache MISS for '{city_name}'")
            return None
            
        except Exception as e:
            print(f"⚠️ Error reading cache: {e}")
            return None
    
    def cache_data(self, city_name, data):
        """
        Store city data in cache.
        
        Args:
            city_name (str): Name of the city
            data (dict): Data to cache (attractions, hotels, restaurants)
        """
        try:
            normalized_city = city_name.lower().strip()
            
            cache_entry = {
                'city_name': normalized_city,
                'data': data,
                'cached_at': datetime.utcnow()
            }
            
            # Upsert: Update if exists, insert if not
            self.cache_collection.update_one(
                {'city_name': normalized_city},
                {'$set': cache_entry},
                upsert=True
            )
            
            print(f"💾 Cached data for '{city_name}'")
            
        except Exception as e:
            print(f"⚠️ Error caching data: {e}")
            # Don't raise - caching failure shouldn't break the app
    
    def clear_cache(self, city_name=None):
        """
        Clear cache for a specific city or all cities.
        
        Args:
            city_name (str, optional): City to clear. If None, clears all.
        """
        try:
            if city_name:
                normalized_city = city_name.lower().strip()
                result = self.cache_collection.delete_one({'city_name': normalized_city})
                print(f"🗑️ Cleared cache for '{city_name}': {result.deleted_count} entries")
            else:
                result = self.cache_collection.delete_many({})
                print(f"🗑️ Cleared all cache: {result.deleted_count} entries")
                
        except Exception as e:
            print(f"⚠️ Error clearing cache: {e}")
    
    def close(self):
        """Close MongoDB connection."""
        self.client.close()
        print("🔌 MongoDB connection closed")


# Singleton instance
db_service = DatabaseService()