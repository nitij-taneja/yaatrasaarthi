from rest_framework import status, viewsets
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from datetime import datetime
import uuid

from .models import ChatSession, ChatMessage, Destination, EcoTip, LocalArtisan
from .serializers import (
    ChatSessionSerializer, ChatMessageSerializer, DestinationSerializer,
    EcoTipSerializer, LocalArtisanSerializer, ChatRequestSerializer,
    ChatResponseSerializer, WeatherRequestSerializer, WeatherResponseSerializer,
    MeditationRequestSerializer, MeditationResponseSerializer
)
from .services import ChatbotService, WeatherService, MeditationService, SentimentAnalysisService
from .services import SustainabilityService, OfflineService
from .llm_service import personalization_service
from .voice_service import voice_service, multilingual_service

class ChatAPIView(APIView):
    """Main chat endpoint"""
    
    def post(self, request):
        serializer = ChatRequestSerializer(data=request.data)
        if serializer.is_valid():
            user_message = serializer.validated_data['message']
            session_id = serializer.validated_data.get('session_id')
            user_context = serializer.validated_data.get('context', {})
            user_id = request.data.get('user_id')
            role = request.data.get('role')
            
            # Create or get session
            if not session_id:
                session_id = str(uuid.uuid4())
            
            session, created = ChatSession.objects.get_or_create(
                session_id=session_id,
                defaults={'session_id': session_id}
            )
            
            # Generate response
            bot_response = ChatbotService.generate_response(
                user_message, user_context, user_id, role
            )
            sentiment = SentimentAnalysisService.analyze_sentiment(user_message)
            
            # Save message
            chat_message = ChatMessage.objects.create(
                session=session,
                user_message=user_message,
                bot_response=bot_response,
                sentiment=sentiment
            )
            
            response_data = {
                "response": bot_response,
                "session_id": session_id,
                "timestamp": chat_message.timestamp,
                "sentiment": sentiment
            }
            
            response_serializer = ChatResponseSerializer(response_data)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VoiceChatAPIView(APIView):
    """Voice chat endpoint"""
    
    def post(self, request):
        try:
            audio_data = request.FILES.get('audio')
            user_id = request.data.get('user_id')
            
            if not audio_data:
                return Response({"error": "Audio data required"}, status=status.HTTP_400_BAD_REQUEST)
            
            # Process voice input
            result = ChatbotService.process_voice_input(audio_data.read(), user_id)
            
            return Response(result, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RoleSwitchAPIView(APIView):
    """Dynamic role switching endpoint"""
    
    def post(self, request):
        try:
            role = request.data.get('role')
            user_id = request.data.get('user_id')
            
            if not role:
                return Response({"error": "Role parameter required"}, status=status.HTTP_400_BAD_REQUEST)
            
            message = ChatbotService.switch_role(role, user_id)
            
            return Response({
                "message": message,
                "active_role": role,
                "timestamp": datetime.now().isoformat()
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PersonalizationAPIView(APIView):
    """User personalization endpoint"""
    
    def post(self, request):
        try:
            user_id = request.data.get('user_id')
            preferences = request.data.get('preferences', {})
            
            if not user_id:
                return Response({"error": "User ID required"}, status=status.HTTP_400_BAD_REQUEST)
            
            # Update user profile
            personalization_service.update_user_profile(user_id, preferences)
            
            # Get personalized recommendations
            recommendations = personalization_service.get_personalized_recommendations(
                user_id, 'activities'
            )
            
            return Response({
                "message": "Preferences updated successfully",
                "recommendations": recommendations,
                "timestamp": datetime.now().isoformat()
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SustainabilityAPIView(APIView):
    """Sustainability and eco-tourism endpoint"""
    
    def post(self, request):
        try:
            action = request.data.get('action')
            
            if action == 'eco_score':
                travel_plan = request.data.get('travel_plan', {})
                score = SustainabilityService.get_eco_impact_score(travel_plan)
                return Response({"eco_score": score}, status=status.HTTP_200_OK)
            
            elif action == 'artisans':
                location = request.data.get('location')
                artisans = SustainabilityService.get_local_artisan_recommendations(location)
                return Response({"artisans": artisans}, status=status.HTTP_200_OK)
            
            elif action == 'carbon_tips':
                journey_type = request.data.get('journey_type', 'pilgrimage')
                tips = SustainabilityService.get_carbon_footprint_tips(journey_type)
                return Response({"tips": tips}, status=status.HTTP_200_OK)
            
            else:
                return Response({"error": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class OfflineAPIView(APIView):
    """Offline functionality endpoint"""
    
    def get(self, request):
        try:
            # Return cached essential data
            cached_data = OfflineService.cache_essential_data()
            return Response(cached_data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request):
        try:
            query = request.data.get('query')
            if not query:
                return Response({"error": "Query required"}, status=status.HTTP_400_BAD_REQUEST)
            
            response = OfflineService.get_offline_response(query)
            
            return Response({
                "response": response,
                "offline_mode": True,
                "timestamp": datetime.now().isoformat()
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class MultilingualAPIView(APIView):
    """Multilingual support endpoint"""
    
    def post(self, request):
        try:
            action = request.data.get('action')
            
            if action == 'detect_language':
                text = request.data.get('text')
                language = multilingual_service.detect_language(text)
                return Response({"detected_language": language}, status=status.HTTP_200_OK)
            
            elif action == 'translate':
                text = request.data.get('text')
                source_lang = request.data.get('source_lang', 'auto')
                target_lang = request.data.get('target_lang', 'en')
                
                if source_lang == 'auto':
                    source_lang = multilingual_service.detect_language(text)
                
                translated = multilingual_service.translate_text(text, source_lang, target_lang)
                
                return Response({
                    "original_text": text,
                    "translated_text": translated,
                    "source_language": source_lang,
                    "target_language": target_lang
                }, status=status.HTTP_200_OK)
            
            elif action == 'greeting':
                language = request.data.get('language', 'en')
                greeting = multilingual_service.get_localized_greeting(language)
                return Response({"greeting": greeting}, status=status.HTTP_200_OK)
            
            else:
                return Response({"error": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class WeatherAPIView(APIView):
    """Weather information endpoint"""
    
    def post(self, request):
        serializer = WeatherRequestSerializer(data=request.data)
        if serializer.is_valid():
            location = serializer.validated_data['location']
            weather_data = WeatherService.get_weather_data(location)
            
            if weather_data:
                response_serializer = WeatherResponseSerializer(weather_data)
                return Response(response_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"error": "Weather data not available"}, 
                    status=status.HTTP_404_NOT_FOUND
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, location=None):
        if location:
            weather_data = WeatherService.get_weather_data(location)
            if weather_data:
                response_serializer = WeatherResponseSerializer(weather_data)
                return Response(response_serializer.data, status=status.HTTP_200_OK)
        
        return Response(
            {"error": "Location parameter required"}, 
            status=status.HTTP_400_BAD_REQUEST
        )

class MeditationAPIView(APIView):
    """Meditation recommendations endpoint"""
    
    def post(self, request):
        serializer = MeditationRequestSerializer(data=request.data)
        if serializer.is_valid():
            user_state = serializer.validated_data['state']
            user_preferences = request.data.get('preferences')
            
            if user_preferences:
                recommendations = MeditationService.get_personalized_meditation(user_state, user_preferences)
            else:
                recommendations = MeditationService.get_recommendations(user_state)
            
            response_serializer = MeditationResponseSerializer(recommendations)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DestinationViewSet(viewsets.ReadOnlyModelViewSet):
    """Destination information viewset"""
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer

class EcoTipViewSet(viewsets.ReadOnlyModelViewSet):
    """Eco-friendly tips viewset"""
    queryset = EcoTip.objects.all()
    serializer_class = EcoTipSerializer

class LocalArtisanViewSet(viewsets.ReadOnlyModelViewSet):
    """Local artisan information viewset"""
    queryset = LocalArtisan.objects.all()
    serializer_class = LocalArtisanSerializer

class ChatSessionViewSet(viewsets.ReadOnlyModelViewSet):
    """Chat session management viewset"""
    queryset = ChatSession.objects.all()
    serializer_class = ChatSessionSerializer
    lookup_field = 'session_id'
    
    @action(detail=True, methods=['get'])
    def messages(self, request, session_id=None):
        """Get all messages for a session"""
        session = get_object_or_404(ChatSession, session_id=session_id)
        messages = session.messages.all()
        serializer = ChatMessageSerializer(messages, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def health_check(request):
    """Health check endpoint"""
    return Response({
        "status": "healthy",
        "service": "YatraSaarthi Django API",
        "timestamp": datetime.now().isoformat()
    })

@api_view(['GET'])
def api_info(request):
    """API information endpoint"""
    return Response({
        "name": "YatraSaarthi API",
        "version": "1.0.0",
        "description": "Advanced multilingual AI chatbot with LLM, RAG, and voice support for spiritual and eco-tourism in India",
        "endpoints": {
            "chat": "/api/chat/",
            "voice_chat": "/api/voice-chat/",
            "role_switch": "/api/role-switch/",
            "personalization": "/api/personalization/",
            "sustainability": "/api/sustainability/",
            "offline": "/api/offline/",
            "multilingual": "/api/multilingual/",
            "weather": "/api/weather/",
            "meditation": "/api/meditation/",
            "destinations": "/api/destinations/",
            "eco-tips": "/api/eco-tips/",
            "artisans": "/api/artisans/",
            "sessions": "/api/sessions/",
            "health": "/api/health/",
        }
    })