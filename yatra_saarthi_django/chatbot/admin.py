from django.contrib import admin
from .models import ChatSession, ChatMessage, Destination, EcoTip, LocalArtisan

@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ['session_id', 'user', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['session_id', 'user__username']

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['session', 'sentiment', 'timestamp']
    list_filter = ['sentiment', 'timestamp']
    search_fields = ['user_message', 'bot_response']

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ['name', 'altitude', 'best_time']
    search_fields = ['name', 'description']

@admin.register(EcoTip)
class EcoTipAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['title', 'description']

@admin.register(LocalArtisan)
class LocalArtisanAdmin(admin.ModelAdmin):
    list_display = ['name', 'craft_type', 'location']
    list_filter = ['craft_type']
    search_fields = ['name', 'craft_type', 'location']