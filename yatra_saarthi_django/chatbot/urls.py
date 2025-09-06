from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'destinations', views.DestinationViewSet)
router.register(r'eco-tips', views.EcoTipViewSet)
router.register(r'artisans', views.LocalArtisanViewSet)
router.register(r'sessions', views.ChatSessionViewSet)

urlpatterns = [
    # API endpoints
    path('chat/', views.ChatAPIView.as_view(), name='chat'),
    path('voice-chat/', views.VoiceChatAPIView.as_view(), name='voice-chat'),
    path('role-switch/', views.RoleSwitchAPIView.as_view(), name='role-switch'),
    path('personalization/', views.PersonalizationAPIView.as_view(), name='personalization'),
    path('sustainability/', views.SustainabilityAPIView.as_view(), name='sustainability'),
    path('offline/', views.OfflineAPIView.as_view(), name='offline'),
    path('multilingual/', views.MultilingualAPIView.as_view(), name='multilingual'),
    path('weather/', views.WeatherAPIView.as_view(), name='weather'),
    path('weather/<str:location>/', views.WeatherAPIView.as_view(), name='weather-location'),
    path('meditation/', views.MeditationAPIView.as_view(), name='meditation'),
    path('health/', views.health_check, name='health'),
    path('info/', views.api_info, name='api-info'),
    
    # ViewSet routes
    path('', include(router.urls)),
]