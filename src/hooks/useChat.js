import { useState, useCallback } from 'react'
import { chatApi } from '../services/api'

export const useChat = () => {
  const [messages, setMessages] = useState([])
  const [sessionId, setSessionId] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState(null)

  const initializeChat = useCallback(() => {
    const welcomeMessage = {
      id: 1,
      user_message: '',
      bot_response: 'Namaste! I\'m YatraSaarthi, your spiritual travel companion. I can help you with information about Char Dham temples, weather updates, eco-friendly travel tips, meditation guidance, and travel planning. What would you like to know about your spiritual journey?',
      timestamp: new Date().toISOString(),
      sentiment: 'peaceful'
    }
    setMessages([welcomeMessage])
  }, [])

  const sendMessage = useCallback(async (message, context = {}) => {
    if (!message.trim()) return

    setIsLoading(true)
    setError(null)

    try {
      const response = await chatApi.sendMessage(message, sessionId, context)
      
      const newMessage = {
        id: Date.now(),
        user_message: message,
        bot_response: response.response,
        timestamp: response.timestamp,
        sentiment: response.sentiment
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
        sentiment: 'neutral'
      }
      
      setMessages(prev => [...prev, errorMessage])
      throw err
    } finally {
      setIsLoading(false)
    }
  }, [sessionId])

  const clearChat = useCallback(() => {
    setMessages([])
    setSessionId('')
    setError(null)
    initializeChat()
  }, [initializeChat])

  return {
    messages,
    sessionId,
    isLoading,
    error,
    sendMessage,
    clearChat,
    initializeChat
  }
}