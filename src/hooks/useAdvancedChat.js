import { useState, useCallback, useRef, useEffect } from 'react'
import { advancedChatApi, multilingualApi } from '../services/advancedApi'

export const useAdvancedChat = (userId = null) => {
  const [messages, setMessages] = useState([])
  const [sessionId, setSessionId] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState(null)
  const [currentRole, setCurrentRole] = useState('travel_companion')
  const [currentLanguage, setCurrentLanguage] = useState('en')
  const [isVoiceEnabled, setIsVoiceEnabled] = useState(false)
  const [isListening, setIsListening] = useState(false)
  
  const mediaRecorderRef = useRef(null)
  const audioChunksRef = useRef([])

  useEffect(() => {
    initializeChat()
  }, [])

  const initializeChat = useCallback(async () => {
    try {
      // Get localized greeting
      const greetingResponse = await multilingualApi.getGreeting(currentLanguage)
      const welcomeMessage = {
        id: 1,
        user_message: '',
        bot_response: greetingResponse.greeting || 'Namaste! I\'m YatraSaarthi, your advanced AI spiritual travel companion with multilingual support, voice interaction, and personalized recommendations.',
        timestamp: new Date().toISOString(),
        sentiment: 'welcoming',
        role: currentRole,
        language: currentLanguage
      }
      setMessages([welcomeMessage])
    } catch (error) {
      console.error('Error initializing chat:', error)
      // Fallback message
      const welcomeMessage = {
        id: 1,
        user_message: '',
        bot_response: 'Namaste! I\'m YatraSaarthi, your advanced AI spiritual travel companion.',
        timestamp: new Date().toISOString(),
        sentiment: 'welcoming',
        role: currentRole,
        language: currentLanguage
      }
      setMessages([welcomeMessage])
    }
  }, [currentLanguage, currentRole])

  const sendMessage = useCallback(async (message, context = {}) => {
    if (!message.trim()) return

    setIsLoading(true)
    setError(null)

    try {
      // Detect language if not set
      if (currentLanguage === 'auto') {
        const langResponse = await multilingualApi.detectLanguage(message)
        setCurrentLanguage(langResponse.detected_language || 'en')
      }

      const response = await advancedChatApi.sendMessage(
        message, 
        sessionId, 
        context, 
        userId, 
        currentRole
      )
      
      const newMessage = {
        id: Date.now(),
        user_message: message,
        bot_response: response.response,
        timestamp: response.timestamp,
        sentiment: response.sentiment,
        role: currentRole,
        language: currentLanguage,
        recommendations: response.recommendations || []
      }

      setMessages(prev => [...prev, newMessage])
      setSessionId(response.session_id)
      
      return response
    } catch (err) {
      setError('Failed to send message. Please try again.')
      
      const errorMessage = {
        id: Date.now(),
        user_message: message,
        bot_response: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date().toISOString(),
        sentiment: 'neutral',
        role: currentRole,
        language: currentLanguage
      }
      
      setMessages(prev => [...prev, errorMessage])
      throw err
    } finally {
      setIsLoading(false)
    }
  }, [sessionId, userId, currentRole, currentLanguage])

  const switchRole = useCallback(async (newRole) => {
    try {
      const response = await advancedChatApi.switchRole(newRole, userId)
      setCurrentRole(newRole)
      
      const roleMessage = {
        id: Date.now(),
        user_message: '',
        bot_response: response.message,
        timestamp: response.timestamp,
        sentiment: 'helpful',
        role: newRole,
        language: currentLanguage,
        isSystemMessage: true
      }
      
      setMessages(prev => [...prev, roleMessage])
      
      return response
    } catch (error) {
      setError('Failed to switch role')
      throw error
    }
  }, [userId, currentLanguage])

  const startVoiceRecording = useCallback(async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      const mediaRecorder = new MediaRecorder(stream)
      mediaRecorderRef.current = mediaRecorder
      audioChunksRef.current = []

      mediaRecorder.ondataavailable = (event) => {
        audioChunksRef.current.push(event.data)
      }

      mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/wav' })
        await sendVoiceMessage(audioBlob)
        stream.getTracks().forEach(track => track.stop())
      }

      mediaRecorder.start()
      setIsListening(true)
    } catch (error) {
      setError('Failed to start voice recording')
      console.error('Voice recording error:', error)
    }
  }, [])

  const stopVoiceRecording = useCallback(() => {
    if (mediaRecorderRef.current && isListening) {
      mediaRecorderRef.current.stop()
      setIsListening(false)
    }
  }, [isListening])

  const sendVoiceMessage = useCallback(async (audioBlob) => {
    setIsLoading(true)
    try {
      const response = await advancedChatApi.sendVoiceMessage(audioBlob, userId)
      
      if (response.error) {
        setError(response.error)
        return
      }

      const voiceMessage = {
        id: Date.now(),
        user_message: response.text_input,
        bot_response: response.response,
        timestamp: new Date().toISOString(),
        sentiment: 'neutral',
        role: currentRole,
        language: response.language,
        isVoiceMessage: true
      }

      setMessages(prev => [...prev, voiceMessage])
    } catch (error) {
      setError('Failed to process voice message')
      console.error('Voice message error:', error)
    } finally {
      setIsLoading(false)
    }
  }, [userId, currentRole])

  const changeLanguage = useCallback(async (newLanguage) => {
    setCurrentLanguage(newLanguage)
    
    // Get greeting in new language
    try {
      const greetingResponse = await multilingualApi.getGreeting(newLanguage)
      const languageMessage = {
        id: Date.now(),
        user_message: '',
        bot_response: greetingResponse.greeting,
        timestamp: new Date().toISOString(),
        sentiment: 'welcoming',
        role: currentRole,
        language: newLanguage,
        isSystemMessage: true
      }
      
      setMessages(prev => [...prev, languageMessage])
    } catch (error) {
      console.error('Error changing language:', error)
    }
  }, [currentRole])

  const clearChat = useCallback(() => {
    setMessages([])
    setSessionId('')
    setError(null)
    initializeChat()
  }, [initializeChat])

  const toggleVoice = useCallback(() => {
    setIsVoiceEnabled(prev => !prev)
  }, [])

  return {
    messages,
    sessionId,
    isLoading,
    error,
    currentRole,
    currentLanguage,
    isVoiceEnabled,
    isListening,
    sendMessage,
    switchRole,
    startVoiceRecording,
    stopVoiceRecording,
    changeLanguage,
    toggleVoice,
    clearChat,
    initializeChat
  }
}