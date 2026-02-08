"""
AI Service for DESTINEX
Generates insights and estimates price ranges using simple keyword logic
No external AI APIs needed - keeps it fast, free, and explainable
"""


class AIService:
    """
    Service class for AI-like features.
    Uses rule-based logic for price estimation and insight generation.
    Fast, free, and completely explainable.
    """
    
    # Keywords for price categorization
    LUXURY_KEYWORDS = [
        'luxury', 'premium', '5-star', 'five star', 'resort', 'palace', 
        'heritage', 'boutique', 'fine dining', 'rooftop', 'spa', 'golf',
        'marriott', 'taj', 'hyatt', 'hilton', 'oberoi', 'itc', 'leela',
        'expensive', 'high-end', 'exclusive', 'private', 'suite'
    ]
    
    BUDGET_KEYWORDS = [
        'budget', 'cheap', 'economy', 'hostel', 'backpacker', 'dhaba',
        'street food', 'cafe', 'inexpensive', 'affordable', 'low-cost',
        'zostel', 'free', 'complimentary', 'no charge'
    ]
    
    MODERATE_KEYWORDS = [
        'mid-range', 'moderate', '3-star', 'three star', 'comfortable',
        'decent', 'reasonable', 'standard', 'regular', 'casual'
    ]
    
    # Insight templates by category
    ATTRACTION_INSIGHTS = {
        'historic': [
            "Rich in history and culture. Best visited with a guide to fully appreciate the stories.",
            "A testament to the region's glorious past. Don't miss the architectural details.",
            "Step back in time and experience the heritage of this magnificent site."
        ],
        'nature': [
            "Perfect escape from city life. Visit early morning for the best experience.",
            "Breathtaking natural beauty. Ideal for photography enthusiasts.",
            "A peaceful retreat surrounded by nature's finest offerings."
        ],
        'religious': [
            "Spiritual ambiance that brings peace and tranquility. Dress modestly.",
            "Important pilgrimage site with deep cultural significance.",
            "Experience the divine atmosphere and architectural grandeur."
        ],
        'entertainment': [
            "Great place for fun and entertainment with family and friends.",
            "Vibrant atmosphere with plenty of activities for all ages.",
            "Perfect spot to unwind and enjoy leisure time."
        ],
        'default': [
            "Popular destination loved by locals and tourists alike.",
            "Worth a visit when exploring the city. Check reviews for best times.",
            "A must-see attraction that captures the essence of the city."
        ]
    }
    
    HOTEL_INSIGHTS = {
        'luxury': [
            "World-class amenities and impeccable service for a memorable stay.",
            "Indulge in luxury with stunning views and premium facilities.",
            "Perfect blend of comfort and elegance for discerning travelers."
        ],
        'boutique': [
            "Charming property with unique character and personalized service.",
            "Intimate setting with attention to every detail.",
            "Experience local hospitality in a cozy, well-appointed space."
        ],
        'budget': [
            "Great value for money with all essential amenities.",
            "Clean and comfortable accommodation without breaking the bank.",
            "Perfect for budget travelers and backpackers."
        ],
        'default': [
            "Convenient location with good amenities for a comfortable stay.",
            "Well-rated property offering reliable hospitality.",
            "Good choice for both business and leisure travelers."
        ]
    }
    
    RESTAURANT_INSIGHTS = {
        'fine_dining': [
            "Exquisite culinary experience with impeccable presentation and service.",
            "Perfect for special occasions with an elegant ambiance.",
            "Mouthwatering dishes crafted by skilled chefs using premium ingredients."
        ],
        'casual': [
            "Relaxed atmosphere with delicious food at reasonable prices.",
            "Great spot for a casual meal with friends and family.",
            "Consistently good food with friendly service."
        ],
        'street_food': [
            "Authentic local flavors that shouldn't be missed.",
            "Popular among locals - a true taste of the city's culinary culture.",
            "Delicious and affordable - perfect for food adventurers."
        ],
        'default': [
            "Well-loved eatery serving tasty dishes in a welcoming setting.",
            "Good food, good vibes - a reliable choice for any meal.",
            "Recommended by locals for its quality and consistency."
        ]
    }
    
    def __init__(self):
        """Initialize the AI service."""
        print("🤖 AI Service initialized (rule-based, no API costs)")
    
    def estimate_price_range(self, name, kinds='', rating=0):
        """
        Estimate price range (₹ / ₹₹ / ₹₹₹) based on name and keywords.
        
        Args:
            name (str): Name of the place
            kinds (str): Category tags from OpenTripMap
            rating (float): Rating value
            
        Returns:
            str: Price range symbol
        """
        text = (name + ' ' + kinds).lower()
        
        # Check for luxury indicators
        if any(keyword in text for keyword in self.LUXURY_KEYWORDS):
            return '₹₹₹'
        
        # Check for budget indicators
        if any(keyword in text for keyword in self.BUDGET_KEYWORDS):
            return '₹'
        
        # Check for moderate indicators
        if any(keyword in text for keyword in self.MODERATE_KEYWORDS):
            return '₹₹'
        
        # Use rating as fallback indicator
        # Higher rated places tend to be more expensive
        if rating >= 4.5:
            return '₹₹₹'
        elif rating >= 4.0:
            return '₹₹'
        else:
            return '₹'
    
    def generate_rating(self, name):
        """
        Generate a procedural rating between 3.5 and 5.0 based on the place name.
        This ensures the rating is consistent for the same place but varies across places.
        """
        import hashlib
        
        # Create a consistent seed from the name
        hash_obj = hashlib.md5(name.encode())
        hash_int = int(hash_obj.hexdigest(), 16)
        
        # Map hash to 3.5 - 5.0 range
        # (hash % 16) gives 0-15. 
        # We want range 1.5 spread (3.5 to 5.0).
        # (0-15) / 10 = 0-1.5 -> + 3.5 = 3.5 - 5.0
        
        variance = (hash_int % 16) / 10.0
        rating = 3.5 + variance
        
        return round(rating, 1)
    
    def categorize_attraction_type(self, kinds):
        """
        Categorize attraction type based on OpenTripMap kinds.
        
        Args:
            kinds (str): Comma-separated kinds from OpenTripMap
            
        Returns:
            str: Category type for insight selection
        """
        kinds_lower = kinds.lower()
        
        if any(k in kinds_lower for k in ['historic', 'cultural', 'architecture', 'monument', 'museum', 'fort', 'palace']):
            return 'historic'
        elif any(k in kinds_lower for k in ['natural', 'park', 'garden', 'beach', 'mountain', 'lake', 'nature']):
            return 'nature'
        elif any(k in kinds_lower for k in ['religion', 'temple', 'church', 'mosque', 'gurdwara', 'shrine', 'spiritual']):
            return 'religious'
        elif any(k in kinds_lower for k in ['amusement', 'entertainment', 'zoo', 'aquarium', 'theater', 'cinema']):
            return 'entertainment'
        else:
            return 'default'
    
    def categorize_hotel_type(self, name, kinds):
        """
        Categorize hotel type for insight selection.
        
        Args:
            name (str): Hotel name
            kinds (str): Kinds from OpenTripMap
            
        Returns:
            str: Hotel category
        """
        text = (name + ' ' + kinds).lower()
        
        if any(k in text for k in ['luxury', 'premium', '5-star', 'resort', 'palace', 'spa']):
            return 'luxury'
        elif any(k in text for k in ['boutique', 'heritage', 'charming', 'unique']):
            return 'boutique'
        elif any(k in text for k in ['hostel', 'budget', 'economy', 'cheap']):
            return 'budget'
        else:
            return 'default'
    
    def categorize_restaurant_type(self, name, kinds):
        """
        Categorize restaurant type for insight selection.
        
        Args:
            name (str): Restaurant name
            kinds (str): Kinds from OpenTripMap
            
        Returns:
            str: Restaurant category
        """
        text = (name + ' ' + kinds).lower()
        
        if any(k in text for k in ['fine dining', 'gourmet', 'luxury', 'premium', '5-star']):
            return 'fine_dining'
        elif any(k in text for k in ['street food', 'fast food', 'food court', 'stall']):
            return 'street_food'
        elif any(k in text for k in ['cafe', 'casual', 'bistro', 'diner']):
            return 'casual'
        else:
            return 'default'
    
    def generate_insight(self, name, category, kinds, rating=0):
        """
        Generate a short AI-like insight for a place.
        
        Args:
            name (str): Name of the place
            category (str): 'attractions', 'hotels', or 'restaurants'
            kinds (str): Kinds from OpenTripMap
            rating (float): Rating value
            
        Returns:
            str: Generated insight
        """
        import random
        
        # Seed random for some variety but consistency per place
        random.seed(hash(name) % 10000)
        
        if category == 'attractions':
            attr_type = self.categorize_attraction_type(kinds)
            insights = self.ATTRACTION_INSIGHTS.get(attr_type, self.ATTRACTION_INSIGHTS['default'])
        
        elif category == 'hotels':
            hotel_type = self.categorize_hotel_type(name, kinds)
            insights = self.HOTEL_INSIGHTS.get(hotel_type, self.HOTEL_INSIGHTS['default'])
        
        elif category == 'restaurants':
            rest_type = self.categorize_restaurant_type(name, kinds)
            insights = self.RESTAURANT_INSIGHTS.get(rest_type, self.RESTAURANT_INSIGHTS['default'])
        
        else:
            return "A great place to visit and explore."
        
        # Add rating-based context
        insight = random.choice(insights)
        
        if rating >= 4.5:
            insight += " Highly rated by visitors!"
        elif rating >= 4.0:
            insight += " Well-loved by travelers."
        
        return insight
    
    def rank_places(self, places):
        """
        Rank places based on rating and popularity.
        
        Args:
            places (list): List of place dictionaries
            
        Returns:
            list: Sorted list of places
        """
        # Sort by rating (descending), then by number of reviews if available
        return sorted(places, key=lambda x: (
            x.get('rating', 0),
            x.get('review_count', 0)
        ), reverse=True)


# Singleton instance
ai_service = AIService()