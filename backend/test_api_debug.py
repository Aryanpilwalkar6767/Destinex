import sys
import os
from dotenv import load_dotenv

# Load env vars first
load_dotenv()

# Add current directory to path so we can import services
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    print("Importing services...")
    from services.place_service import place_service
    print("Services imported.")
except Exception as e:
    print(f"Failed to import services: {e}")
    sys.exit(1)

def test_api():
    city = "Dadar, Mumbai" # Testing the user's query
    print(f"Testing search for {city} (Geoapify)...")
    
    # 1. Test Geocoding
    print("1. Testing Geocoding (Geoapify)...")
    lat, lon, display_name = None, None, None
    try:
        lat, lon, display_name = place_service.get_coordinates(city)
        print(f"   Result: lat={lat}, lon={lon}, name={display_name}")
    except Exception as e:
        print(f"   ❌ Geocoding raised exception: {e}")

    if not lat:
        print("   ❌ Geocoding failed. Aborting.")
        return

    # 2. Test Attractions
    print("\n2. Testing Attractions...")
    try:
        attractions = place_service.get_attractions(lat, lon, limit=5)
        print(f"   Found {len(attractions)} attractions.")
        if attractions: print(f"   Sample: {attractions[0]}")
    except Exception as e:
        print(f"   ❌ Attractions Error: {e}")

    # 3. Test Hotels
    print("\n3. Testing Hotels...")
    try:
        hotels = place_service.get_hotels(lat, lon, limit=5)
        print(f"   Found {len(hotels)} hotels.")
        if hotels: print(f"   Sample: {hotels[0]}")
    except Exception as e:
        print(f"   ❌ Hotels Error: {e}")

    # 4. Test Restaurants
    print("\n4. Testing Restaurants...")
    try:
        restaurants = place_service.get_restaurants(lat, lon, limit=5)
        print(f"   Found {len(restaurants)} restaurants.")
        if restaurants: print(f"   Sample: {restaurants[0]}")
    except Exception as e:
        print(f"   ❌ Restaurants Error: {e}")

if __name__ == "__main__":
    test_api()
