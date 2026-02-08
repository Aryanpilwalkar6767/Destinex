"""
DESTINEX Backend Application
Main Flask application with REST API endpoints
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add services directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.place_service import place_service
from services.ai_service import ai_service
from services.db_service import db_service

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for frontend communication
CORS(app, resources={
    r"/search": {
        "origins": ["http://localhost:5500", "http://127.0.0.1:5500", 
                   "http://localhost:5000", "http://127.0.0.1:5000", "*"]
    }
})

# Configuration
app.config['JSON_SORT_KEYS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


def format_place_data(raw_places, category):
    """
    Format raw place data into the required response structure.
    Add AI-generated insights and price ranges.
    
    Args:
        raw_places (list): Raw places from API
        category (str): Category name
        
    Returns:
        list: Formatted places
    """
    formatted = []
    
    for place in raw_places:
        # Skip places without names
        if not place.get('name'):
            continue
        
        # Get AI-generated insight
        insight = ai_service.generate_insight(
            name=place['name'],
            category=category,
            kinds=place.get('kinds', ''),
            rating=place.get('rating', 0)
        )
        
        # Estimate price range
        price_range = ai_service.estimate_price_range(
            name=place['name'],
            kinds=place.get('kinds', ''),
            rating=place.get('rating', 0)
        )
        
        # Generate procedural rating (since API doesn't provide it)
        rating = ai_service.generate_rating(place['name'])
        
        formatted_place = {
            'name': place['name'],
            'category': category[:-1] if category.endswith('s') else category,  # singular
            'rating': rating,
            'price_range': price_range,
            'ai_insight': insight,
            'distance': place.get('distance', 0),
            'lat': place.get('lat'),
            'lon': place.get('lon')
        }
        
        formatted.append(formatted_place)
    
    # Rank by rating
    return ai_service.rank_places(formatted)


@app.route('/')
def home():
    """Root endpoint - API info."""
    return jsonify({
        'app': 'DESTINEX API',
        'version': '1.0',
        'description': 'AI-powered travel discovery backend',
        'endpoints': {
            '/search?city=<city_name>': 'Search for attractions, hotels, and restaurants in a city'
        },
        'status': 'running'
    })


@app.route('/search', methods=['GET'])
def search():
    """
    Main search endpoint.
    
    Query Parameters:
        city (str): Name of the city to search
        
    Returns:
        JSON with attractions, hotels, and restaurants
    """
    # Get city parameter
    city = request.args.get('city', '').strip()
    
    # Validate input
    if not city:
        return jsonify({
            'success': False,
            'error': 'City name is required. Use: /search?city=CityName',
            'attractions': [],
            'hotels': [],
            'restaurants': []
        }), 400
    
    print(f"\n{'='*50}")
    print(f"🔍 SEARCH REQUEST: {city}")
    print(f"{'='*50}")
    
    # Check cache first
    cached_data = db_service.get_cached_data(city)
    if cached_data:
        return jsonify({
            'success': True,
            'city': city,
            'cached': True,
            **cached_data
        })
    
    # Get coordinates for the city
    lat, lon, display_name = place_service.get_coordinates(city)
    
    if lat is None or lon is None:
        return jsonify({
            'success': False,
            'error': f"Could not find coordinates for '{city}'. Please check the city name and try again.",
            'attractions': [],
            'hotels': [],
            'restaurants': []
        }), 404
    
    try:
        # Fetch data from APIs
        print("\n📍 Fetching attractions...")
        raw_attractions = place_service.get_attractions(lat, lon, limit=10)
        
        print("\n🏨 Fetching hotels...")
        raw_hotels = place_service.get_hotels(lat, lon, limit=8)
        
        print("\n🍽️ Fetching restaurants...")
        raw_restaurants = place_service.get_restaurants(lat, lon, limit=10)
        
        # Format and enhance data
        attractions = format_place_data(raw_attractions, 'attractions')
        hotels = format_place_data(raw_hotels, 'hotels')
        restaurants = format_place_data(raw_restaurants, 'restaurants')
        
        # Prepare response
        response_data = {
            'attractions': attractions,
            'hotels': hotels,
            'restaurants': restaurants
        }
        
        # Cache the results
        db_service.cache_data(city, response_data)
        
        print(f"\n✅ Search complete for '{city}'")
        print(f"   - {len(attractions)} attractions")
        print(f"   - {len(hotels)} hotels")
        print(f"   - {len(restaurants)} restaurants")
        print(f"{'='*50}\n")
        
        return jsonify({
            'success': True,
            'city': display_name or city,
            'cached': False,
            **response_data
        })
        
    except Exception as e:
        print(f"❌ Error processing search: {e}")
        return jsonify({
            'success': False,
            'error': f"An error occurred while fetching data: {str(e)}",
            'attractions': [],
            'hotels': [],
            'restaurants': []
        }), 500


@app.route('/clear-cache', methods=['POST'])
def clear_cache():
    """
    Admin endpoint to clear cache.
    
    Query Parameters:
        city (str, optional): Specific city to clear. If not provided, clears all.
    """
    city = request.args.get('city')
    db_service.clear_cache(city)
    
    return jsonify({
        'success': True,
        'message': f"Cache cleared{' for ' + city if city else ' for all cities'}"
    })


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        'success': False,
        'error': 'Endpoint not found. Use /search?city=CityName',
        'attractions': [],
        'hotels': [],
        'restaurants': []
    }), 404


@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors."""
    return jsonify({
        'success': False,
        'error': 'Internal server error. Please try again later.',
        'attractions': [],
        'hotels': [],
        'restaurants': []
    }), 500


if __name__ == '__main__':
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║   🌟 DESTINEX Backend Server 🌟                         ║
    ║   AI-Powered Travel Discovery API                        ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
    
    📋 Prerequisites:
       1. MongoDB must be running locally (mongod)
       2. Python dependencies: pip install -r requirements.txt
    
    🚀 Starting server...
    """)
    
    # Run the Flask app
    app.run(
    host='0.0.0.0',
    port=5000,
    debug=False,
    use_reloader=False
    )
