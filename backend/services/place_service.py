"""
Place Service for DESTINEX - GEOAPIFY VERSION
"""

import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class PlaceService:
    GEOAPIFY_BASE_URL = "https://api.geoapify.com/v2/places"
    GEOAPIFY_GEOCODE_URL = "https://api.geoapify.com/v1/geocode/search"
    
    # Get API key from environment variable
    GEOAPIFY_API_KEY = os.getenv("GEOAPIFY_API_KEY")

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'DESTINEX-Travel-App/1.0'})
        print("🌍 Place Service initialized (Geoapify)")
        
        if not self.GEOAPIFY_API_KEY:
            print("❌ ERROR: GEOAPIFY_API_KEY not found in environment variables!")

    def get_coordinates(self, city_name):
        """Convert city name to lat/lon using Geoapify Geocoding."""
        try:
            params = {
                'text': city_name,
                'apiKey': self.GEOAPIFY_API_KEY,
                'limit': 1
            }
            
            response = self.session.get(self.GEOAPIFY_GEOCODE_URL, params=params, timeout=10)
            data = response.json()
            
            if not data or not data.get('features'):
                return None, None, None
            
            feature = data['features'][0]
            props = feature['properties']
            
            lat = props.get('lat')
            lon = props.get('lon')
            display_name = props.get('formatted')
            
            return lat, lon, display_name
            
        except Exception as e:
            print(f"❌ Geocoding error: {e}")
            return None, None, None

    def calculate_distance(self, lat1, lon1, lat2, lon2):
        """
        Calculate the great circle distance between two points 
        on the earth (specified in decimal degrees) using Haversine formula.
        """
        import math
        
        # Convert decimal degrees to radians 
        lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])

        # Haversine formula 
        dlon = lon2 - lon1 
        dlat = lat2 - lat1 
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a)) 
        r = 6371 # Radius of earth in kilometers. Use 3956 for miles.
        return c * r

    def fetch_places_from_geoapify(self, lat, lon, categories, limit=20, radius=5000):
        """
        Fetch places from Geoapify Places API.
        """
        if not self.GEOAPIFY_API_KEY:
            print("❌ Cannot fetch places: Missing API Key")
            return []
            
        try:
            params = {
                'categories': categories,
                'filter': f'circle:{lon},{lat},{radius}',
                'limit': limit,
                'apiKey': self.GEOAPIFY_API_KEY
            }
            
            print(f"🔍 Geoapify: categories={categories}, radius={radius}m")
            
            response = self.session.get(self.GEOAPIFY_BASE_URL, params=params, timeout=15)
            
            if response.status_code != 200:
                print(f"❌ API Error {response.status_code}: {response.text}")
                return []
                
            data = response.json()
            
            if not data or not data.get('features'):
                print(f"⚠️ No data returned")
                return []
            
            places = []
            for feature in data['features']:
                props = feature['properties']
                
                # Basic validation
                if not props.get('name'):
                    continue
                    
                place_lat = props.get('lat')
                place_lon = props.get('lon')
                
                # Calculate distance if missing
                dist = props.get('distance', 0) / 1000.0
                if dist == 0 and place_lat and place_lon:
                    dist = self.calculate_distance(lat, lon, place_lat, place_lon)
                
                # Extract relevant fields
                place = {
                    'name': props.get('name'),
                    'address': props.get('formatted'),
                    'lat': place_lat,
                    'lon': place_lon,
                    'categories': props.get('categories', []),
                    'kinds': ','.join(props.get('categories', [])),
                    'distance': round(dist, 2)
                }
                
                # Geoapify typically doesn't return ratings in the free tier
                place['rating'] = 0 
                
                places.append(place)
            
            print(f"✅ Found {len(places)} places")
            return places
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return []

    def get_attractions(self, lat, lon, limit=15):
        """Get tourist attractions."""
        print("\n📍 Fetching attractions...")
        categories = "tourism"
        return self.fetch_places_from_geoapify(lat, lon, categories, limit=limit)

    def get_hotels(self, lat, lon, limit=10):
        """Get hotels."""
        print("\n🏨 Fetching hotels...")
        categories = "accommodation"
        return self.fetch_places_from_geoapify(lat, lon, categories, limit=limit)

    def get_restaurants(self, lat, lon, limit=15):
        """Get restaurants."""
        print("\n🍽️ Fetching restaurants...")
        categories = "catering"
        return self.fetch_places_from_geoapify(lat, lon, categories, limit=limit)


# Singleton instance
place_service = PlaceService()
