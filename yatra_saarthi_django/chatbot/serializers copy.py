from rest_framework import serializers
from .models import ChatSession, ChatMessage, Destination, EcoTip, LocalArtisan

class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['id', 'user_message', 'bot_response', 'timestamp', 'sentiment']

class ChatSessionSerializer(serializers.ModelSerializer):
    messages = ChatMessageSerializer(many=True, read_only=True)
    
    class Meta:
        model = ChatSession
        fields = ['id', 'session_id', 'created_at', 'updated_at', 'messages']

class DestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = ['id', 'name', 'description', 'best_time', 'altitude', 'mythology', 'latitude', 'longitude']

class EcoTipSerializer(serializers.ModelSerializer):
    class Meta:
        model = EcoTip
        fields = ['id', 'title', 'description', 'category', 'created_at']

class LocalArtisanSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocalArtisan
        fields = ['id', 'name', 'craft_type', 'location', 'contact_info', 'description']

class ChatRequestSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=1000)
    session_id = serializers.CharField(max_length=100, required=False)
    context = serializers.JSONField(required=False)

class ChatResponseSerializer(serializers.Serializer):
    response = serializers.CharField()
    session_id = serializers.CharField()
    timestamp = serializers.DateTimeField()
    sentiment = serializers.CharField(required=False)

class WeatherRequestSerializer(serializers.Serializer):
    location = serializers.CharField(max_length=100)

class WeatherResponseSerializer(serializers.Serializer):
    temperature = serializers.FloatField()
    description = serializers.CharField()
    humidity = serializers.IntegerField()
    wind_speed = serializers.FloatField()
    location = serializers.CharField()

class MeditationRequestSerializer(serializers.Serializer):
    state = serializers.CharField(max_length=500)

class MeditationResponseSerializer(serializers.Serializer):
    sentiment = serializers.CharField()
    recommendations = serializers.ListField(child=serializers.CharField())

