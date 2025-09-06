from flask import Blueprint, jsonify, request
import requests
import json
import os
from datetime import datetime

chatbot_bp = Blueprint('chatbot', __name__)

# Free APIs configuration
WEATHER_API_KEY = "your_openweather_api_key"  # Replace with actual API key
WEATHER_BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

# Tourism data for Char Dham circuit
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

def get_weather_data(location):
    """Get weather data for a location"""
    try:
        if WEATHER_API_KEY == "your_openweather_api_key":
            # Return mock data if no API key
            return {
                "temperature": 15,
                "description": "Clear sky",
                "humidity": 65,
                "wind_speed": 5.2
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
                "wind_speed": data["wind"]["speed"]
            }
    except Exception as e:
        print(f"Weather API error: {e}")
    
    return None

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

def generate_response(user_message, user_context=None):
    """Generate chatbot response based on user message"""
    message_lower = user_message.lower()
    
    # Weather queries
    if "weather" in message_lower:
        for location, data in CHAR_DHAM_DATA.items():
            if location in message_lower or data["name"].lower() in message_lower:
                weather = get_weather_data(data["name"])
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
        import random
        tip = random.choice(ECO_TIPS)
        return f"Here's an eco-friendly travel tip: {tip}. Sustainable tourism helps preserve these sacred places for future generations!"
    
    # Meditation recommendations
    if "meditation" in message_lower or "stress" in message_lower or "relax" in message_lower:
        sentiment = analyze_sentiment(user_message)
        recommendations = MEDITATION_RECOMMENDATIONS.get(sentiment, MEDITATION_RECOMMENDATIONS["peaceful"])
        import random
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

@chatbot_bp.route('/chat', methods=['POST'])
def chat():
    """Main chat endpoint"""
    try:
        data = request.json
        user_message = data.get('message', '')
        user_context = data.get('context', {})
        
        if not user_message:
            return jsonify({"error": "Message is required"}), 400
        
        response = generate_response(user_message, user_context)
        
        return jsonify({
            "response": response,
            "timestamp": datetime.now().isoformat(),
            "context": user_context
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@chatbot_bp.route('/destinations', methods=['GET'])
def get_destinations():
    """Get information about Char Dham destinations"""
    return jsonify(CHAR_DHAM_DATA)

@chatbot_bp.route('/weather/<location>', methods=['GET'])
def get_weather(location):
    """Get weather for a specific location"""
    weather_data = get_weather_data(location)
    if weather_data:
        return jsonify(weather_data)
    else:
        return jsonify({"error": "Weather data not available"}), 404

@chatbot_bp.route('/eco-tips', methods=['GET'])
def get_eco_tips():
    """Get eco-friendly travel tips"""
    return jsonify({"tips": ECO_TIPS})

@chatbot_bp.route('/meditation', methods=['POST'])
def get_meditation_recommendation():
    """Get meditation recommendation based on user's current state"""
    try:
        data = request.json
        user_state = data.get('state', '')
        
        sentiment = analyze_sentiment(user_state)
        recommendations = MEDITATION_RECOMMENDATIONS.get(sentiment, MEDITATION_RECOMMENDATIONS["peaceful"])
        
        return jsonify({
            "sentiment": sentiment,
            "recommendations": recommendations
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@chatbot_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "YatraSaarthi Chatbot",
        "timestamp": datetime.now().isoformat()
    })

