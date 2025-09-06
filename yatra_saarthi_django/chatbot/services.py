import requests
import random
from datetime import datetime
from .models import Destination, EcoTip, LocalArtisan
from .llm_service import llm_service, personalization_service
from .voice_service import voice_service, multilingual_service

# Free APIs configuration
WEATHER_API_KEY = "your_openweather_api_key"  # Replace with actual API key
WEATHER_BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

# Char Dham data
CHAR_DHAM_DATA = {
    "badrinath": {
        "name": "Badrinath",
        "description": "One of the four sacred Char Dham pilgrimage sites dedicated to Lord Vishnu",
        "best_time": "May to October",
        "altitude": "3,133 meters",
        "mythology": "According to Hindu mythology, Lord Vishnu meditated here under a Badri tree",
        "location": {"lat": 30.7433, "lon": 79.4938}
    },
    "kedarnath": {
        "name": "Kedarnath",
        "description": "Sacred temple dedicated to Lord Shiva, one of the twelve Jyotirlingas",
        "best_time": "May to October",
        "altitude": "3,583 meters",
        "mythology": "Legend says the Pandavas built this temple to seek Lord Shiva's forgiveness",
        "location": {"lat": 30.7346, "lon": 79.0669}
    },
    "gangotri": {
        "name": "Gangotri",
        "description": "Source of the holy river Ganga, sacred to Hindus",
        "best_time": "May to October",
        "altitude": "3,100 meters",
        "mythology": "King Bhagirath meditated here to bring Ganga to earth",
        "location": {"lat": 30.9993, "lon": 78.9411}
    },
    "yamunotri": {
        "name": "Yamunotri",
        "description": "Source of the Yamuna river, dedicated to Goddess Yamuna",
        "best_time": "May to October",
        "altitude": "3,293 meters",
        "mythology": "Sage Asit Muni resided here and bathed daily in both Ganga and Yamuna",
        "location": {"lat": 31.0117, "lon": 78.4270}
    }
}

# Eco-tourism tips
ECO_TIPS = [
    "Carry reusable water bottles to reduce plastic waste",
    "Use biodegradable soaps and shampoos",
    "Stick to marked trails to protect vegetation",
    "Pack out all trash, leave no trace",
    "Respect local wildlife and maintain distance",
    "Support local homestays and businesses",
    "Use public transport or shared vehicles when possible",
    "Avoid single-use plastics",
    "Respect local customs and traditions",
    "Conserve water and electricity in accommodations"
]

# Meditation recommendations based on sentiment
MEDITATION_RECOMMENDATIONS = {
    "stressed": [
        "Try deep breathing exercises for 5-10 minutes",
        "Practice progressive muscle relaxation",
        "Listen to calming nature sounds",
        "Focus on gratitude meditation"
    ],
    "anxious": [
        "Practice mindful breathing",
        "Try body scan meditation",
        "Use grounding techniques (5-4-3-2-1 method)",
        "Practice loving-kindness meditation"
    ],
    "excited": [
        "Channel energy with walking meditation",
        "Practice gratitude meditation",
        "Try visualization techniques",
        "Focus on present moment awareness"
    ],
    "peaceful": [
        "Deepen your practice with longer sessions",
        "Try silent meditation",
        "Practice contemplative meditation",
        "Explore different meditation styles"
    ]
}

class WeatherService:
    @staticmethod
    def get_weather_data(location):
        """Get weather data for a location"""
        try:
            if WEATHER_API_KEY == "your_openweather_api_key":
                # Return mock data if no API key
                return {
                    "temperature": 15,
                    "description": "Clear sky",
                    "humidity": 65,
                    "wind_speed": 5.2,
                    "location": location
                }
            
            params = {
                "q": location,
                "appid": WEATHER_API_KEY,
                "units": "metric"
            }
            response = requests.get(WEATHER_BASE_URL, params=params, timeout=5)
            if response.status_code == 200:
                data = response.json()
                return {
                    "temperature": data["main"]["temp"],
                    "description": data["weather"][0]["description"],
                    "humidity": data["main"]["humidity"],
                    "wind_speed": data["wind"]["speed"],
                    "location": location
                }
        except Exception as e:
            print(f"Weather API error: {e}")
        
        return None

class SentimentAnalysisService:
    @staticmethod
    def analyze_sentiment(text):
        """Simple sentiment analysis based on keywords"""
        text_lower = text.lower()
        
        stress_keywords = ["stress", "worried", "anxious", "nervous", "overwhelmed", "tired"]
        anxiety_keywords = ["scared", "fear", "panic", "worry", "uncertain"]
        excitement_keywords = ["excited", "happy", "thrilled", "amazing", "wonderful", "great"]
        peaceful_keywords = ["calm", "peaceful", "relaxed", "serene", "tranquil"]
        
        if any(word in text_lower for word in stress_keywords):
            return "stressed"
        elif any(word in text_lower for word in anxiety_keywords):
            return "anxious"
        elif any(word in text_lower for word in excitement_keywords):
            return "excited"
        elif any(word in text_lower for word in peaceful_keywords):
            return "peaceful"
        
        return "neutral"

class ChatbotService:
    @staticmethod
    def generate_response(user_message, user_context=None, user_id=None, role=None):
        """Generate chatbot response based on user message"""
        
        # Determine role dynamically if not specified
        if not role:
            role = personalization_service.determine_role(user_message, user_context or {})
        
        # Use advanced LLM service for response generation
        try:
            llm_response = llm_service.generate_response(
                user_message, 
                user_context or {}, 
                role
            )
            
            # Add personalized recommendations if user_id provided
            if user_id:
                recommendations = personalization_service.get_personalized_recommendations(
                    user_id, 'activities'
                )
                if recommendations:
                    llm_response['recommendations'] = recommendations
            
            return llm_response['response']
            
        except Exception as e:
            # Fallback to rule-based system
            return ChatbotService._fallback_response(user_message, user_context)
    
    @staticmethod
    def _fallback_response(user_message, user_context=None):
        """Fallback rule-based response system"""
        message_lower = user_message.lower()
        
        # Weather queries
        if "weather" in message_lower:
            for location, data in CHAR_DHAM_DATA.items():
                if location in message_lower or data["name"].lower() in message_lower:
                    weather = WeatherService.get_weather_data(data["name"])
                    if weather:
                        return f"Current weather in {data['name']}: {weather['temperature']}°C, {weather['description']}. Humidity: {weather['humidity']}%, Wind: {weather['wind_speed']} m/s. {data['name']} is best visited from {data['best_time']}."
                    else:
                        return f"I couldn't get current weather data for {data['name']}, but generally {data['name']} is best visited from {data['best_time']}."
        
        # Char Dham information
        for location, data in CHAR_DHAM_DATA.items():
            if location in message_lower or data["name"].lower() in message_lower:
                return f"{data['name']}: {data['description']}. Located at {data['altitude']} altitude. Best time to visit: {data['best_time']}. Mythology: {data['mythology']}"
        
        # Eco-tourism tips
        if any(word in message_lower for word in ["eco", "environment", "sustainable", "green", "tips"]):
            tip = random.choice(ECO_TIPS)
            return f"Here's an eco-friendly travel tip: {tip}. Sustainable tourism helps preserve these sacred places for future generations!"
        
        # Meditation recommendations
        if "meditation" in message_lower or "stress" in message_lower or "relax" in message_lower:
            sentiment = SentimentAnalysisService.analyze_sentiment(user_message)
            recommendations = MEDITATION_RECOMMENDATIONS.get(sentiment, MEDITATION_RECOMMENDATIONS["peaceful"])
            recommendation = random.choice(recommendations)
            return f"Based on how you're feeling, I recommend: {recommendation}. Taking time for mindfulness can enhance your spiritual journey."
        
        # Yoga recommendations
        if "yoga" in message_lower:
            return "For your spiritual journey, try these yoga practices: Morning Sun Salutations to energize, Mountain Pose for grounding, and Pranayama (breathing exercises) for mental clarity. Practice with respect for the sacred environment around you."
        
        # Homestay information
        if "homestay" in message_lower or "accommodation" in message_lower:
            return "I recommend staying in local homestays to support the community and experience authentic culture. Look for family-run guesthouses in villages near the temples. They often provide home-cooked meals and valuable local insights."
        
        # General travel planning
        if any(word in message_lower for word in ["plan", "itinerary", "route", "travel"]):
            return "For Char Dham Yatra, I recommend this sequence: Yamunotri → Gangotri → Kedarnath → Badrinath. Allow 10-12 days total. Start early in the season (May) for better weather. Book accommodations in advance and carry warm clothing even in summer."
        
        # Default response
        return "Namaste! I'm YatraSaarthi, your spiritual travel companion. I can help you with information about Char Dham temples, weather updates, eco-friendly travel tips, meditation guidance, and travel planning. What would you like to know about your spiritual journey?"
    
    @staticmethod
    def process_voice_input(audio_data, user_id=None):
        """Process voice input and return response"""
        try:
            # Convert speech to text
            text = voice_service.speech_to_text(audio_data)
            if not text:
                return {"error": "Could not understand speech"}
            
            # Detect language
            detected_lang = multilingual_service.detect_language(text)
            
            # Generate response
            response = ChatbotService.generate_response(text, {}, user_id)
            
            # Convert response to speech
            voice_service.text_to_speech(response, detected_lang)
            
            return {
                "text_input": text,
                "response": response,
                "language": detected_lang,
                "voice_enabled": True
            }
            
        except Exception as e:
            return {"error": f"Voice processing error: {str(e)}"}
    
    @staticmethod
    def get_multilingual_greeting(language='en'):
        """Get greeting in specified language"""
        return multilingual_service.get_localized_greeting(language)
    
    @staticmethod
    def switch_role(new_role, user_id=None):
        """Switch chatbot role dynamically"""
        valid_roles = ['travel_companion', 'cultural_expert', 'spiritual_guide', 'eco_advocate', 'travel_planner']
        
        if new_role not in valid_roles:
            return f"Invalid role. Available roles: {', '.join(valid_roles)}"
        
        role_messages = {
            'cultural_expert': "🏛️ I'm now in Cultural Expert mode. I can share deep insights about history, traditions, and mythology of sacred places.",
            'spiritual_guide': "🕉️ I'm now in Spiritual Guide mode. Let me help you with meditation, prayers, and spiritual practices.",
            'eco_advocate': "🌱 I'm now in Eco Advocate mode. I'll focus on sustainable travel and environmental protection.",
            'travel_planner': "🗺️ I'm now in Travel Planner mode. I'll help with itineraries, bookings, and logistics.",
            'travel_companion': "🤝 I'm back to being your general travel companion, ready to help with anything!"
        }
        
        return role_messages.get(new_role, "Role switched successfully!")

class MeditationService:
    @staticmethod
    def get_recommendations(user_state):
        """Get meditation recommendations based on user's current state"""
        sentiment = SentimentAnalysisService.analyze_sentiment(user_state)
        recommendations = MEDITATION_RECOMMENDATIONS.get(sentiment, MEDITATION_RECOMMENDATIONS["peaceful"])
        return {
            "sentiment": sentiment,
            "recommendations": recommendations
        }
    
    @staticmethod
    def get_personalized_meditation(user_state, user_preferences=None):
        """Get personalized meditation based on user state and preferences"""
        sentiment = SentimentAnalysisService.analyze_sentiment(user_state)
        base_recommendations = MEDITATION_RECOMMENDATIONS.get(sentiment, MEDITATION_RECOMMENDATIONS["peaceful"])
        
        # Customize based on user preferences
        if user_preferences:
            if user_preferences.get('experience_level') == 'beginner':
                base_recommendations = [rec for rec in base_recommendations if 'simple' in rec.lower() or 'basic' in rec.lower()]
            elif user_preferences.get('time_available', 0) < 10:
                base_recommendations = [rec for rec in base_recommendations if '5-10 minutes' in rec or 'quick' in rec.lower()]
        
        return {
            "sentiment": sentiment,
            "recommendations": base_recommendations,
            "personalized": True
        }

class SustainabilityService:
    """Advanced sustainability and eco-tourism features"""
    
    @staticmethod
    def get_eco_impact_score(travel_plan):
        """Calculate eco-impact score for travel plan"""
        score = 100  # Start with perfect score
        
        # Deduct points for non-eco choices
        if travel_plan.get('transport') == 'private_car':
            score -= 20
        elif travel_plan.get('transport') == 'shared_vehicle':
            score -= 10
        
        if travel_plan.get('accommodation') == 'hotel':
            score -= 15
        elif travel_plan.get('accommodation') == 'homestay':
            score += 10
        
        if travel_plan.get('plastic_free', False):
            score += 15
        
        return max(0, min(100, score))
    
    @staticmethod
    def get_local_artisan_recommendations(location):
        """Get local artisan recommendations for location"""
        artisan_data = {
            'badrinath': [
                {
                    'name': 'Ramesh Kumar',
                    'craft': 'Wood Carving',
                    'specialty': 'Religious sculptures',
                    'location': 'Near Badrinath Temple',
                    'contact': 'Available at local market'
                }
            ],
            'kedarnath': [
                {
                    'name': 'Sunita Devi',
                    'craft': 'Handwoven Textiles',
                    'specialty': 'Garhwali shawls',
                    'location': 'Kedarnath Valley',
                    'contact': 'Through local homestays'
                }
            ]
        }
        
        return artisan_data.get(location.lower(), [])
    
    @staticmethod
    def get_carbon_footprint_tips(journey_type):
        """Get carbon footprint reduction tips"""
        tips = {
            'pilgrimage': [
                "Use shared transportation to reduce individual carbon footprint",
                "Choose vegetarian meals to reduce environmental impact",
                "Carry reusable water bottles and avoid single-use plastics",
                "Offset your carbon footprint by supporting local tree plantation"
            ],
            'trekking': [
                "Use eco-friendly camping gear and biodegradable products",
                "Follow Leave No Trace principles strictly",
                "Support local guides and porters for community benefit",
                "Choose established campsites to minimize environmental impact"
            ]
        }
        
        return tips.get(journey_type, tips['pilgrimage'])

class OfflineService:
    """Handle offline functionality and data caching"""
    
    @staticmethod
    def cache_essential_data():
        """Cache essential data for offline use"""
        essential_data = {
            'destinations': list(Destination.objects.all().values()),
            'eco_tips': list(EcoTip.objects.all().values()),
            'emergency_contacts': {
                'police': '100',
                'medical': '108',
                'tourist_helpline': '1363'
            },
            'basic_phrases': {
                'help': {'hi': 'मदद', 'en': 'help'},
                'water': {'hi': 'पानी', 'en': 'water'},
                'food': {'hi': 'खाना', 'en': 'food'},
                'temple': {'hi': 'मंदिर', 'en': 'temple'}
            }
        }
        
        return essential_data
    
    @staticmethod
    def get_offline_response(query):
        """Generate response using cached data only"""
        cached_data = OfflineService.cache_essential_data()
        
        query_lower = query.lower()
        
        if 'emergency' in query_lower:
            contacts = cached_data['emergency_contacts']
            return f"Emergency contacts: Police: {contacts['police']}, Medical: {contacts['medical']}, Tourist Helpline: {contacts['tourist_helpline']}"
        
        if any(dest in query_lower for dest in ['badrinath', 'kedarnath', 'gangotri', 'yamunotri']):
            destinations = cached_data['destinations']
            for dest in destinations:
                if dest['name'].lower() in query_lower:
                    return f"{dest['name']}: {dest['description']} Best time: {dest['best_time']}"
        
        return "I'm currently offline. I can help with basic destination info and emergency contacts. For detailed assistance, please connect to internet."