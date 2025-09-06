import React, { useState, useEffect, useRef } from 'react'
import { Button } from './ui/button'
import { Input } from './ui/input'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card'
import { Badge } from './ui/badge'
import { MessageCircle, Send, Loader2 } from 'lucide-react'
import { useChat } from '../hooks/useChat'
import { SENTIMENT_COLORS } from '../utils/constants'

const ChatInterface = () => {
  const { messages, isLoading, error, sendMessage, initializeChat } = useChat()
  const [inputMessage, setInputMessage] = useState('')
  const messagesEndRef = useRef(null)

  useEffect(() => {
    initializeChat()
  }, [initializeChat])

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const handleSendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return

    const message = inputMessage
    setInputMessage('')
    
    try {
      await sendMessage(message)
    } catch (error) {
      console.error('Failed to send message:', error)
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

  const getSentimentColor = (sentiment) => {
    return SENTIMENT_COLORS[sentiment] || SENTIMENT_COLORS.neutral
  }

  return (
    <Card className="h-full flex flex-col">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <MessageCircle className="w-5 h-5 text-orange-600" />
          Chat with YatraSaarthi
        </CardTitle>
        <CardDescription>
          Ask me about Char Dham temples, travel planning, meditation, or eco-friendly tips
        </CardDescription>
      </CardHeader>
      
      <CardContent className="flex-1 flex flex-col">
        {/* Messages Container */}
        <div className="flex-1 space-y-4 mb-4 max-h-96 overflow-y-auto p-2 border rounded-lg bg-gray-50">
          {messages.map((message) => (
            <div key={message.id} className="space-y-2">
              {/* User Message */}
              {message.user_message && (
                <div className="flex justify-end">
                  <div className="bg-orange-500 text-white p-3 rounded-lg max-w-xs lg:max-w-md shadow-sm">
                    <p className="text-sm">{message.user_message}</p>
                  </div>
                </div>
              )}
              
              {/* Bot Response */}
              <div className="flex justify-start">
                <div className="bg-white border p-3 rounded-lg max-w-xs lg:max-w-md shadow-sm">
                  <p className="text-sm text-gray-800 mb-2">{message.bot_response}</p>
                  
                  {/* Sentiment Badge */}
                  {message.sentiment && (
                    <div className="flex items-center justify-between">
                      <Badge className={`text-xs ${getSentimentColor(message.sentiment)}`}>
                        {message.sentiment}
                      </Badge>
                      <span className="text-xs text-gray-500">
                        {new Date(message.timestamp).toLocaleTimeString()}
                      </span>
                    </div>
                  )}
                </div>
              </div>
            </div>
          ))}
          
          {/* Loading Indicator */}
          {isLoading && (
            <div className="flex justify-start">
              <div className="bg-white border p-3 rounded-lg shadow-sm">
                <div className="flex items-center gap-2">
                  <Loader2 className="w-4 h-4 animate-spin text-orange-500" />
                  <span className="text-sm text-gray-600">YatraSaarthi is thinking...</span>
                </div>
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>

        {/* Error Message */}
        {error && (
          <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg">
            <p className="text-sm text-red-600">{error}</p>
          </div>
        )}
        
        {/* Input Area */}
        <div className="flex gap-2">
          <Input
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            placeholder="Ask me about your spiritual journey..."
            onKeyPress={handleKeyPress}
            disabled={isLoading}
            className="flex-1"
          />
          <Button 
            onClick={handleSendMessage} 
            disabled={isLoading || !inputMessage.trim()}
            className="px-4"
          >
            {isLoading ? (
              <Loader2 className="w-4 h-4 animate-spin" />
            ) : (
              <Send className="w-4 h-4" />
            )}
          </Button>
        </div>
      </CardContent>
    </Card>
  )
}

export default ChatInterface