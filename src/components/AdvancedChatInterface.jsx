import React, { useState, useEffect, useRef } from 'react'
import { Button } from './ui/button'
import { Input } from './ui/input'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card'
import { Badge } from './ui/badge'
import { 
  MessageCircle, 
  Send, 
  Loader2, 
  Mic, 
  MicOff, 
  Volume2, 
  VolumeX,
  Globe,
  UserCog,
  Sparkles,
  Leaf,
  Map,
  Heart
} from 'lucide-react'
import { useAdvancedChat } from '../hooks/useAdvancedChat'
import { SENTIMENT_COLORS } from '../utils/constants'

const AdvancedChatInterface = ({ userId = null }) => {
  const { 
    messages, 
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
    initializeChat 
  } = useAdvancedChat(userId)
  
  const [inputMessage, setInputMessage] = useState('')
  const [showRoleSelector, setShowRoleSelector] = useState(false)
  const [showLanguageSelector, setShowLanguageSelector] = useState(false)
  const messagesEndRef = useRef(null)

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

  const handleRoleSwitch = async (newRole) => {
    try {
      await switchRole(newRole)
      setShowRoleSelector(false)
    } catch (error) {
      console.error('Failed to switch role:', error)
    }
  }

  const handleLanguageChange = async (newLanguage) => {
    try {
      await changeLanguage(newLanguage)
      setShowLanguageSelector(false)
    } catch (error) {
      console.error('Failed to change language:', error)
    }
  }

  const handleVoiceToggle = () => {
    if (isListening) {
      stopVoiceRecording()
    } else {
      startVoiceRecording()
    }
  }

  const getSentimentColor = (sentiment) => {
    return SENTIMENT_COLORS[sentiment] || SENTIMENT_COLORS.neutral
  }

  const getRoleIcon = (role) => {
    const icons = {
      'travel_companion': <MessageCircle className="w-4 h-4" />,
      'cultural_expert': <Sparkles className="w-4 h-4" />,
      'spiritual_guide': <Heart className="w-4 h-4" />,
      'eco_advocate': <Leaf className="w-4 h-4" />,
      'travel_planner': <Map className="w-4 h-4" />
    }
    return icons[role] || <MessageCircle className="w-4 h-4" />
  }

  const getRoleColor = (role) => {
    const colors = {
      'travel_companion': 'bg-blue-500',
      'cultural_expert': 'bg-purple-500',
      'spiritual_guide': 'bg-orange-500',
      'eco_advocate': 'bg-green-500',
      'travel_planner': 'bg-indigo-500'
    }
    return colors[role] || 'bg-blue-500'
  }

  const availableRoles = [
    { id: 'travel_companion', name: 'Travel Companion', description: 'General travel assistance' },
    { id: 'cultural_expert', name: 'Cultural Expert', description: 'History and traditions' },
    { id: 'spiritual_guide', name: 'Spiritual Guide', description: 'Meditation and spirituality' },
    { id: 'eco_advocate', name: 'Eco Advocate', description: 'Sustainable travel' },
    { id: 'travel_planner', name: 'Travel Planner', description: 'Itinerary and logistics' }
  ]

  const availableLanguages = [
    { code: 'en', name: 'English' },
    { code: 'hi', name: 'हिंदी (Hindi)' },
    { code: 'pa', name: 'ਪੰਜਾਬੀ (Punjabi)' },
    { code: 'gu', name: 'ગુજરાતી (Gujarati)' },
    { code: 'ta', name: 'தமிழ் (Tamil)' },
    { code: 'te', name: 'తెలుగు (Telugu)' },
    { code: 'kn', name: 'ಕನ್ನಡ (Kannada)' },
    { code: 'ml', name: 'മലയാളം (Malayalam)' },
    { code: 'mr', name: 'मराठी (Marathi)' },
    { code: 'bn', name: 'বাংলা (Bengali)' }
  ]

  return (
    <Card className="h-full flex flex-col">
      <CardHeader>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <MessageCircle className="w-5 h-5 text-orange-600" />
            <CardTitle>Advanced YatraSaarthi Chat</CardTitle>
          </div>
          
          {/* Control Panel */}
          <div className="flex items-center gap-2">
            {/* Role Selector */}
            <div className="relative">
              <Button
                variant="outline"
                size="sm"
                onClick={() => setShowRoleSelector(!showRoleSelector)}
                className={`${getRoleColor(currentRole)} text-white hover:opacity-80`}
              >
                {getRoleIcon(currentRole)}
                <UserCog className="w-3 h-3 ml-1" />
              </Button>
              
              {showRoleSelector && (
                <div className="absolute top-full right-0 mt-2 w-64 bg-white border rounded-lg shadow-lg z-10">
                  <div className="p-2">
                    <h4 className="font-semibold text-sm mb-2">Switch Role</h4>
                    {availableRoles.map((role) => (
                      <button
                        key={role.id}
                        onClick={() => handleRoleSwitch(role.id)}
                        className={`w-full text-left p-2 rounded hover:bg-gray-100 ${
                          currentRole === role.id ? 'bg-blue-50 border-l-4 border-blue-500' : ''
                        }`}
                      >
                        <div className="flex items-center gap-2">
                          {getRoleIcon(role.id)}
                          <div>
                            <div className="font-medium text-sm">{role.name}</div>
                            <div className="text-xs text-gray-500">{role.description}</div>
                          </div>
                        </div>
                      </button>
                    ))}
                  </div>
                </div>
              )}
            </div>

            {/* Language Selector */}
            <div className="relative">
              <Button
                variant="outline"
                size="sm"
                onClick={() => setShowLanguageSelector(!showLanguageSelector)}
              >
                <Globe className="w-4 h-4" />
                <span className="ml-1 text-xs">{currentLanguage.toUpperCase()}</span>
              </Button>
              
              {showLanguageSelector && (
                <div className="absolute top-full right-0 mt-2 w-48 bg-white border rounded-lg shadow-lg z-10 max-h-64 overflow-y-auto">
                  <div className="p-2">
                    <h4 className="font-semibold text-sm mb-2">Select Language</h4>
                    {availableLanguages.map((lang) => (
                      <button
                        key={lang.code}
                        onClick={() => handleLanguageChange(lang.code)}
                        className={`w-full text-left p-2 rounded hover:bg-gray-100 text-sm ${
                          currentLanguage === lang.code ? 'bg-blue-50 border-l-4 border-blue-500' : ''
                        }`}
                      >
                        {lang.name}
                      </button>
                    ))}
                  </div>
                </div>
              )}
            </div>

            {/* Voice Toggle */}
            <Button
              variant="outline"
              size="sm"
              onClick={toggleVoice}
              className={isVoiceEnabled ? 'bg-green-50 text-green-600' : ''}
            >
              {isVoiceEnabled ? <Volume2 className="w-4 h-4" /> : <VolumeX className="w-4 h-4" />}
            </Button>
          </div>
        </div>
        
        <CardDescription>
          <div className="flex items-center gap-2 text-sm">
            <span>Mode: <strong>{availableRoles.find(r => r.id === currentRole)?.name}</strong></span>
            <span>•</span>
            <span>Language: <strong>{availableLanguages.find(l => l.code === currentLanguage)?.name}</strong></span>
            {isVoiceEnabled && (
              <>
                <span>•</span>
                <span className="text-green-600">🎤 Voice Enabled</span>
              </>
            )}
          </div>
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
                    {message.isVoiceMessage && (
                      <div className="flex items-center gap-1 mt-1 text-xs opacity-75">
                        <Mic className="w-3 h-3" />
                        <span>Voice</span>
                      </div>
                    )}
                  </div>
                </div>
              )}
              
              {/* Bot Response */}
              <div className="flex justify-start">
                <div className="bg-white border p-3 rounded-lg max-w-xs lg:max-w-md shadow-sm">
                  <div className="flex items-center gap-2 mb-2">
                    <div className={`w-6 h-6 rounded-full ${getRoleColor(message.role)} flex items-center justify-center text-white`}>
                      {getRoleIcon(message.role)}
                    </div>
                    <span className="text-xs font-medium text-gray-600">
                      {availableRoles.find(r => r.id === message.role)?.name}
                    </span>
                  </div>
                  
                  <p className="text-sm text-gray-800 mb-2">{message.bot_response}</p>
                  
                  {/* Recommendations */}
                  {message.recommendations && message.recommendations.length > 0 && (
                    <div className="mt-2 p-2 bg-blue-50 rounded text-xs">
                      <strong>Recommendations:</strong>
                      <ul className="list-disc list-inside mt-1">
                        {message.recommendations.map((rec, idx) => (
                          <li key={idx}>{rec}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                  
                  {/* Metadata */}
                  <div className="flex items-center justify-between mt-2">
                    {message.sentiment && (
                      <Badge className={`text-xs ${getSentimentColor(message.sentiment)}`}>
                        {message.sentiment}
                      </Badge>
                    )}
                    <div className="flex items-center gap-2 text-xs text-gray-500">
                      {message.language && message.language !== 'en' && (
                        <span className="bg-gray-100 px-1 rounded">{message.language}</span>
                      )}
                      <span>{new Date(message.timestamp).toLocaleTimeString()}</span>
                    </div>
                  </div>
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
            placeholder={`Ask me about your spiritual journey... (${currentLanguage})`}
            onKeyPress={handleKeyPress}
            disabled={isLoading}
            className="flex-1"
          />
          
          {/* Voice Input Button */}
          {isVoiceEnabled && (
            <Button
              onClick={handleVoiceToggle}
              disabled={isLoading}
              className={`px-4 ${isListening ? 'bg-red-500 hover:bg-red-600' : 'bg-green-500 hover:bg-green-600'}`}
            >
              {isListening ? <MicOff className="w-4 h-4" /> : <Mic className="w-4 h-4" />}
            </Button>
          )}
          
          {/* Send Button */}
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

export default AdvancedChatInterface