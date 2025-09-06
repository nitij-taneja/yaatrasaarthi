import os
import json
import random
from typing import List, Dict, Any, Optional
from datetime import datetime
import requests
from sentence_transformers import SentenceTransformer
import chromadb
from googletrans import Translator
import logging

logger = logging.getLogger(__name__)

class LLMService:
    """Advanced LLM service with RAG capabilities"""
    
    def __init__(self):
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.chroma_client = chromadb.Client()
        self.translator = Translator()
        self.collection = None
        self.initialize_knowledge_base()
    
    def initialize_knowledge_base(self):
        """Initialize the RAG knowledge base"""
        try:
            # Create or get collection
            self.collection = self.chroma_client.get_or_create_collection(
                name="yatra_saarthi_knowledge",
                metadata={"description": "YatraSaarthi tourism knowledge base"}
            )
            
            # Add initial knowledge if collection is empty
            if self.collection.count() == 0:
                self.populate_knowledge_base()
                
        except Exception as e:
            logger.error(f"Error initializing knowledge base: {e}")
    
    def populate_knowledge_base(self):
        """Populate the knowledge base with tourism data"""
        knowledge_data = [
            {
                "id": "badrinath_info",
                "content": "Badrinath is one of the four sacred Char Dham pilgrimage sites dedicated to Lord Vishnu. Located at 3,133 meters altitude, it's best visited from May to October. According to Hindu mythology, Lord Vishnu meditated here under a Badri tree. The temple is surrounded by snow-capped peaks and offers spiritual solace to millions of devotees.",
                "category": "destination",
                "location": "Badrinath",
                "metadata": {"type": "pilgrimage", "altitude": "3133m", "deity": "Vishnu"}
            },
            {
                "id": "kedarnath_info",
                "content": "Kedarnath is a sacred temple dedicated to Lord Shiva, one of the twelve Jyotirlingas. Located at 3,583 meters altitude, it's accessible from May to October. Legend says the Pandavas built this temple to seek Lord Shiva's forgiveness after the Kurukshetra war. The temple survived the 2013 floods miraculously.",
                "category": "destination",
                "location": "Kedarnath",
                "metadata": {"type": "pilgrimage", "altitude": "3583m", "deity": "Shiva"}
            },
            {
                "id": "eco_tips_plastic",
                "content": "Carry reusable water bottles and avoid single-use plastics. The Himalayas are fragile ecosystems that take decades to decompose plastic waste. Use biodegradable soaps and shampoos to protect mountain water sources. Pack out all trash following Leave No Trace principles.",
                "category": "eco_tips",
                "metadata": {"type": "sustainability", "focus": "waste_management"}
            },
            {
                "id": "meditation_stress",
                "content": "For stress relief during travel, try the 4-7-8 breathing technique: Inhale for 4 counts, hold for 7, exhale for 8. Practice progressive muscle relaxation starting from your toes. The mountain air and spiritual atmosphere enhance meditation effectiveness.",
                "category": "wellness",
                "metadata": {"type": "meditation", "condition": "stress"}
            },
            {
                "id": "local_artisans_uttarakhand",
                "content": "Uttarakhand is famous for wood carving, handwoven textiles, and stone sculptures. Support local artisans by purchasing authentic Garhwali shawls, wooden temple decorations, and traditional jewelry. Visit local markets near temples for genuine handicrafts.",
                "category": "artisans",
                "metadata": {"type": "crafts", "region": "Uttarakhand"}
            },
            {
                "id": "multilingual_greetings",
                "content": "Namaste (Hindi/Sanskrit), Namaskar (formal Hindi), Sat Sri Akal (Punjabi), Adaab (Urdu), Vanakkam (Tamil), Namaskara (Kannada). Learning local greetings shows respect for regional culture and enhances your spiritual journey experience.",
                "category": "culture",
                "metadata": {"type": "language", "focus": "greetings"}
            }
        ]
        
        # Add documents to collection
        for doc in knowledge_data:
            self.collection.add(
                documents=[doc["content"]],
                metadatas=[doc["metadata"]],
                ids=[doc["id"]]
            )
    
    def detect_language(self, text: str) -> str:
        """Detect the language of input text"""
        try:
            detected = self.translator.detect(text)
            return detected.lang
        except:
            return 'en'  # Default to English
    
    def translate_text(self, text: str, target_lang: str = 'en') -> str:
        """Translate text to target language"""
        try:
            if target_lang == 'en':
                return text
            translated = self.translator.translate(text, dest=target_lang)
            return translated.text
        except:
            return text
    
    def retrieve_relevant_context(self, query: str, n_results: int = 3) -> List[str]:
        """Retrieve relevant context using RAG"""
        try:
            if not self.collection:
                return []
            
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )
            
            return results['documents'][0] if results['documents'] else []
        except Exception as e:
            logger.error(f"Error retrieving context: {e}")
            return []
    
    def generate_response(self, user_message: str, user_context: Dict = None, role: str = "travel_companion") -> Dict[str, Any]:
        """Generate intelligent response using LLM with RAG"""
        
        # Detect language
        detected_lang = self.detect_language(user_message)
        
        # Translate to English for processing if needed
        english_query = user_message
        if detected_lang != 'en':
            english_query = self.translate_text(user_message, 'en')
        
        # Retrieve relevant context
        context_docs = self.retrieve_relevant_context(english_query)
        
        # Generate response based on role and context
        response = self._generate_contextual_response(
            english_query, context_docs, role, user_context or {}
        )
        
        # Translate response back if needed
        if detected_lang != 'en':
            response['response'] = self.translate_text(response['response'], detected_lang)
        
        response['detected_language'] = detected_lang
        response['context_used'] = len(context_docs) > 0
        
        return response
    
    def _generate_contextual_response(self, query: str, context: List[str], role: str, user_context: Dict) -> Dict[str, Any]:
        """Generate response based on context and role"""
        
        query_lower = query.lower()
        
        # Role-based response generation
        if role == "cultural_expert":
            return self._generate_cultural_response(query_lower, context)
        elif role == "spiritual_guide":
            return self._generate_spiritual_response(query_lower, context)
        elif role == "eco_advocate":
            return self._generate_eco_response(query_lower, context)
        elif role == "travel_planner":
            return self._generate_travel_response(query_lower, context)
        else:
            return self._generate_general_response(query_lower, context)
    
    def _generate_cultural_response(self, query: str, context: List[str]) -> Dict[str, Any]:
        """Generate culturally rich responses"""
        
        cultural_responses = {
            "history": "The Char Dham circuit has been a sacred pilgrimage route for over 1,000 years. Each temple represents a different aspect of Hindu spirituality and connects to ancient Vedic traditions.",
            "mythology": "According to the Puranas, these sacred sites were established by great sages and are mentioned in ancient scriptures like the Skanda Purana and Mahabharata.",
            "traditions": "Pilgrims traditionally follow specific rituals: purification baths, offering prayers at dawn, and circumambulation of the temples. Local customs vary but respect for nature is universal."
        }
        
        for key, response in cultural_responses.items():
            if key in query:
                return {
                    "response": response,
                    "sentiment": "enlightened",
                    "role": "cultural_expert",
                    "confidence": 0.9
                }
        
        return {
            "response": "As a cultural expert, I can share the rich heritage of these sacred lands. What specific aspect of our cultural traditions interests you?",
            "sentiment": "knowledgeable",
            "role": "cultural_expert",
            "confidence": 0.7
        }
    
    def _generate_spiritual_response(self, query: str, context: List[str]) -> Dict[str, Any]:
        """Generate spiritually focused responses"""
        
        if any(word in query for word in ["meditation", "peace", "spiritual", "divine"]):
            return {
                "response": "In these sacred mountains, find a quiet spot facing the peaks. Close your eyes and breathe deeply. The ancient vibrations of countless prayers enhance your spiritual practice. Om Namah Shivaya resonates through these valleys.",
                "sentiment": "peaceful",
                "role": "spiritual_guide",
                "confidence": 0.95
            }
        
        if any(word in query for word in ["prayer", "worship", "blessing"]):
            return {
                "response": "Begin your prayers at dawn when the mountains glow golden. Offer water to the deity, light incense, and chant with devotion. The divine presence is strongest in the early morning hours.",
                "sentiment": "devotional",
                "role": "spiritual_guide",
                "confidence": 0.9
            }
        
        return {
            "response": "These sacred peaks have witnessed millions of prayers. What spiritual guidance do you seek on your divine journey?",
            "sentiment": "serene",
            "role": "spiritual_guide",
            "confidence": 0.8
        }
    
    def _generate_eco_response(self, query: str, context: List[str]) -> Dict[str, Any]:
        """Generate eco-focused responses"""
        
        eco_tips = [
            "Use biodegradable soaps to protect mountain streams. The Ganga and Yamuna sources are pristine and must remain so.",
            "Carry reusable water bottles. Plastic waste takes 450 years to decompose in these cold mountain conditions.",
            "Stay on marked trails to prevent soil erosion. Every step off-trail damages fragile alpine vegetation.",
            "Support local homestays to distribute tourism benefits directly to mountain communities.",
            "Use solar chargers for devices. Reduce dependence on diesel generators in remote areas."
        ]
        
        return {
            "response": f"🌱 {random.choice(eco_tips)} Sustainable tourism preserves these sacred places for future generations.",
            "sentiment": "responsible",
            "role": "eco_advocate",
            "confidence": 0.85
        }
    
    def _generate_travel_response(self, query: str, context: List[str]) -> Dict[str, Any]:
        """Generate travel planning responses"""
        
        if "itinerary" in query or "plan" in query:
            return {
                "response": "Optimal Char Dham sequence: Yamunotri (2 days) → Gangotri (2 days) → Kedarnath (3 days) → Badrinath (3 days). Total: 12-14 days. Book helicopters in advance for Kedarnath. Carry warm clothes even in summer.",
                "sentiment": "organized",
                "role": "travel_planner",
                "confidence": 0.9
            }
        
        if "accommodation" in query or "stay" in query:
            return {
                "response": "Book GMVN guesthouses or dharamshalas near temples. Private homestays offer authentic experiences. Advance booking essential during peak season (May-June, Sep-Oct).",
                "sentiment": "helpful",
                "role": "travel_planner",
                "confidence": 0.85
            }
        
        return {
            "response": "I can help plan your perfect pilgrimage! What specific travel arrangements do you need assistance with?",
            "sentiment": "efficient",
            "role": "travel_planner",
            "confidence": 0.8
        }
    
    def _generate_general_response(self, query: str, context: List[str]) -> Dict[str, Any]:
        """Generate general responses with context"""
        
        # Use context if available
        if context:
            context_text = " ".join(context[:2])  # Use first 2 context documents
            return {
                "response": f"Based on my knowledge: {context_text[:200]}... How can I help you further with your spiritual journey?",
                "sentiment": "helpful",
                "role": "travel_companion",
                "confidence": 0.8
            }
        
        # Default response
        return {
            "response": "Namaste! I'm YatraSaarthi, your AI spiritual travel companion. I can help with Char Dham information, eco-friendly tips, cultural insights, and travel planning. What would you like to explore?",
            "sentiment": "welcoming",
            "role": "travel_companion",
            "confidence": 0.7
        }

class PersonalizationService:
    """Handle user personalization and dynamic role switching"""
    
    def __init__(self):
        self.user_profiles = {}
        self.interaction_history = {}
    
    def update_user_profile(self, user_id: str, preferences: Dict):
        """Update user preferences"""
        if user_id not in self.user_profiles:
            self.user_profiles[user_id] = {}
        
        self.user_profiles[user_id].update(preferences)
    
    def get_personalized_recommendations(self, user_id: str, category: str) -> List[str]:
        """Get personalized recommendations based on user profile"""
        
        profile = self.user_profiles.get(user_id, {})
        interests = profile.get('interests', [])
        
        recommendations = {
            'meditation': {
                'spiritual': ["Guided meditation at temple premises", "Sunrise meditation facing peaks"],
                'adventure': ["Walking meditation on trails", "Breathing exercises during treks"],
                'nature': ["Forest meditation", "River-side mindfulness practice"]
            },
            'activities': {
                'spiritual': ["Temple visits", "Aarti participation", "Scripture reading"],
                'adventure': ["Trekking", "River rafting", "Rock climbing"],
                'cultural': ["Local festivals", "Artisan workshops", "Traditional cooking"]
            }
        }
        
        if category in recommendations:
            relevant_recs = []
            for interest in interests:
                if interest in recommendations[category]:
                    relevant_recs.extend(recommendations[category][interest])
            
            return relevant_recs[:3] if relevant_recs else recommendations[category].get('spiritual', [])
        
        return []
    
    def determine_role(self, query: str, user_context: Dict) -> str:
        """Determine appropriate role based on query and context"""
        
        query_lower = query.lower()
        
        if any(word in query_lower for word in ['culture', 'history', 'tradition', 'mythology']):
            return 'cultural_expert'
        elif any(word in query_lower for word in ['spiritual', 'meditation', 'prayer', 'divine']):
            return 'spiritual_guide'
        elif any(word in query_lower for word in ['eco', 'environment', 'sustainable', 'green']):
            return 'eco_advocate'
        elif any(word in query_lower for word in ['plan', 'itinerary', 'book', 'travel', 'route']):
            return 'travel_planner'
        else:
            return 'travel_companion'

# Global instances
llm_service = LLMService()
personalization_service = PersonalizationService()