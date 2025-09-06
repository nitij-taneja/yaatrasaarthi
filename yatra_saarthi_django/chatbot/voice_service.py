import os
import json
import logging
from typing import Optional, Dict, Any
import speech_recognition as sr
import pyttsx3
from googletrans import Translator
import threading
import queue

logger = logging.getLogger(__name__)

class VoiceService:
    """Handle speech-to-text and text-to-speech functionality"""
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.tts_engine = pyttsx3.init()
        self.translator = Translator()
        self.setup_tts()
        
        # Voice processing queue
        self.voice_queue = queue.Queue()
        self.is_listening = False
        
    def setup_tts(self):
        """Configure text-to-speech engine"""
        try:
            # Set voice properties
            voices = self.tts_engine.getProperty('voices')
            if voices:
                # Prefer female voice if available
                for voice in voices:
                    if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                        self.tts_engine.setProperty('voice', voice.id)
                        break
                else:
                    self.tts_engine.setProperty('voice', voices[0].id)
            
            # Set speech rate and volume
            self.tts_engine.setProperty('rate', 150)  # Slower for clarity
            self.tts_engine.setProperty('volume', 0.8)
            
        except Exception as e:
            logger.error(f"Error setting up TTS: {e}")
    
    def speech_to_text(self, audio_data: bytes = None, language: str = 'hi-IN') -> Optional[str]:
        """Convert speech to text"""
        try:
            if audio_data:
                # Process provided audio data
                audio = sr.AudioData(audio_data, 16000, 2)
            else:
                # Record from microphone
                with self.microphone as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=1)
                    logger.info("Listening for speech...")
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
            # Recognize speech with multiple language support
            languages_to_try = [language, 'en-US', 'hi-IN']
            
            for lang in languages_to_try:
                try:
                    text = self.recognizer.recognize_google(audio, language=lang)
                    logger.info(f"Recognized text in {lang}: {text}")
                    return text
                except sr.UnknownValueError:
                    continue
                except sr.RequestError as e:
                    logger.error(f"Speech recognition error for {lang}: {e}")
                    continue
            
            return None
            
        except Exception as e:
            logger.error(f"Speech to text error: {e}")
            return None
    
    def text_to_speech(self, text: str, language: str = 'en', voice_type: str = 'female') -> bool:
        """Convert text to speech"""
        try:
            # Handle different languages
            if language != 'en':
                # For non-English, we might need to transliterate or use different TTS
                pass
            
            # Add natural pauses and emphasis for spiritual content
            enhanced_text = self.enhance_speech_text(text)
            
            # Speak the text
            self.tts_engine.say(enhanced_text)
            self.tts_engine.runAndWait()
            
            return True
            
        except Exception as e:
            logger.error(f"Text to speech error: {e}")
            return False
    
    def enhance_speech_text(self, text: str) -> str:
        """Enhance text for better speech synthesis"""
        
        # Add pauses for better flow
        enhanced = text.replace('.', '... ')
        enhanced = enhanced.replace(',', ', ')
        enhanced = enhanced.replace('!', '! ')
        enhanced = enhanced.replace('?', '? ')
        
        # Emphasize spiritual terms
        spiritual_terms = {
            'Namaste': 'Nah-mas-tay',
            'Badrinath': 'Bad-ree-naath',
            'Kedarnath': 'Kay-dar-naath',
            'Gangotri': 'Gang-oh-tree',
            'Yamunotri': 'Yam-un-oh-tree',
            'Om': 'Aum',
            'Shiva': 'Shee-va',
            'Vishnu': 'Vish-nu'
        }
        
        for term, pronunciation in spiritual_terms.items():
            enhanced = enhanced.replace(term, pronunciation)
        
        return enhanced
    
    def detect_wake_word(self, audio_data: bytes) -> bool:
        """Detect wake word 'Hey YatraSaarthi'"""
        try:
            text = self.speech_to_text(audio_data)
            if text:
                wake_phrases = ['hey yatra saarthi', 'yatra saarthi', 'hey saarthi']
                text_lower = text.lower()
                return any(phrase in text_lower for phrase in wake_phrases)
            return False
        except:
            return False
    
    def start_continuous_listening(self, callback_function):
        """Start continuous listening for voice commands"""
        def listen_continuously():
            self.is_listening = True
            while self.is_listening:
                try:
                    with self.microphone as source:
                        self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                        audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                    
                    # Check for wake word
                    if self.detect_wake_word(audio.frame_data):
                        # Wake word detected, process full command
                        text = self.speech_to_text()
                        if text:
                            callback_function(text)
                
                except sr.WaitTimeoutError:
                    pass  # Continue listening
                except Exception as e:
                    logger.error(f"Continuous listening error: {e}")
        
        # Start listening in background thread
        listen_thread = threading.Thread(target=listen_continuously)
        listen_thread.daemon = True
        listen_thread.start()
    
    def stop_listening(self):
        """Stop continuous listening"""
        self.is_listening = False
    
    def get_supported_languages(self) -> Dict[str, str]:
        """Get supported languages for voice interaction"""
        return {
            'en-US': 'English (US)',
            'hi-IN': 'Hindi (India)',
            'en-IN': 'English (India)',
            'pa-IN': 'Punjabi (India)',
            'gu-IN': 'Gujarati (India)',
            'ta-IN': 'Tamil (India)',
            'te-IN': 'Telugu (India)',
            'kn-IN': 'Kannada (India)',
            'ml-IN': 'Malayalam (India)',
            'mr-IN': 'Marathi (India)',
            'bn-IN': 'Bengali (India)'
        }

class MultilingualService:
    """Handle multilingual support and translation"""
    
    def __init__(self):
        self.translator = Translator()
        self.supported_languages = {
            'en': 'English',
            'hi': 'Hindi',
            'pa': 'Punjabi',
            'gu': 'Gujarati',
            'ta': 'Tamil',
            'te': 'Telugu',
            'kn': 'Kannada',
            'ml': 'Malayalam',
            'mr': 'Marathi',
            'bn': 'Bengali',
            'ur': 'Urdu'
        }
        
        # Regional greetings
        self.greetings = {
            'en': 'Namaste! Welcome to YatraSaarthi',
            'hi': 'नमस्ते! यात्रा सारथी में आपका स्वागत है',
            'pa': 'ਸਤ ਸ੍ਰੀ ਅਕਾਲ! ਯਾਤਰਾ ਸਾਰਥੀ ਵਿੱਚ ਤੁਹਾਡਾ ਸੁਆਗਤ ਹੈ',
            'gu': 'નમસ્તે! યાત્રા સારથીમાં તમારું સ્વાગત છે',
            'ta': 'வணக்கம்! யாத்ரா சாரதியில் உங்களை வரவேற்கிறோம்',
            'te': 'నమస్కారం! యాత్రా సారథిలో మీకు స్వాగతం',
            'kn': 'ನಮಸ್ಕಾರ! ಯಾತ್ರಾ ಸಾರಥಿಗೆ ನಿಮಗೆ ಸ್ವಾಗತ',
            'ml': 'നമസ്കാരം! യാത്രാ സാരഥിയിലേക്ക് സ്വാഗതം',
            'mr': 'नमस्कार! यात्रा सारथीमध्ये तुमचे स्वागत आहे',
            'bn': 'নমস্কার! যাত্রা সারথিতে আপনাকে স্বাগতম',
            'ur': 'آداب! یاترا سارتھی میں آپ کا خوش آمدید'
        }
    
    def detect_language(self, text: str) -> str:
        """Detect language of input text"""
        try:
            detected = self.translator.detect(text)
            return detected.lang if detected.lang in self.supported_languages else 'en'
        except:
            return 'en'
    
    def translate_text(self, text: str, source_lang: str, target_lang: str) -> str:
        """Translate text between languages"""
        try:
            if source_lang == target_lang:
                return text
            
            result = self.translator.translate(text, src=source_lang, dest=target_lang)
            return result.text
        except Exception as e:
            logger.error(f"Translation error: {e}")
            return text
    
    def get_localized_greeting(self, language: str) -> str:
        """Get greeting in specified language"""
        return self.greetings.get(language, self.greetings['en'])
    
    def get_cultural_context(self, language: str) -> Dict[str, Any]:
        """Get cultural context for language"""
        cultural_contexts = {
            'hi': {
                'greeting_style': 'formal_respectful',
                'religious_terms': ['भगवान', 'मंदिर', 'पूजा', 'आरती'],
                'cultural_notes': 'Use respectful language for deities and elders'
            },
            'pa': {
                'greeting_style': 'warm_community',
                'religious_terms': ['गुरु', 'गुरुद्वारा', 'सेवा'],
                'cultural_notes': 'Emphasize community service and sharing'
            },
            'ta': {
                'greeting_style': 'traditional_respectful',
                'religious_terms': ['கடவுள்', 'கோயில்', 'பூஜை'],
                'cultural_notes': 'Respect for Tamil traditions and temple customs'
            }
        }
        
        return cultural_contexts.get(language, {
            'greeting_style': 'universal_respectful',
            'religious_terms': [],
            'cultural_notes': 'Universal spiritual respect'
        })

# Global instances
voice_service = VoiceService()
multilingual_service = MultilingualService()