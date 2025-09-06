const API_BASE_URL = 'http://localhost:8000/api'

class AdvancedApiService {
  static async request(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    }

    try {
      const response = await fetch(url, config)
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      return await response.json()
    } catch (error) {
      console.error('API request failed:', error)
      throw error
    }
  }

  static async post(endpoint, data) {
    return this.request(endpoint, {
      method: 'POST',
      body: JSON.stringify(data),
    })
  }

  static async get(endpoint) {
    return this.request(endpoint, { method: 'GET' })
  }
}

// Advanced Chat API with LLM and RAG
export const advancedChatApi = {
  sendMessage: (message, sessionId = null, context = {}, userId = null, role = null) =>
    AdvancedApiService.post('/chat/', { 
      message, 
      session_id: sessionId, 
      context,
      user_id: userId,
      role 
    }),
  
  sendVoiceMessage: async (audioBlob, userId = null) => {
    const formData = new FormData()
    formData.append('audio', audioBlob)
    if (userId) formData.append('user_id', userId)
    
    const response = await fetch(`${API_BASE_URL}/voice-chat/`, {
      method: 'POST',
      body: formData,
    })
    
    return await response.json()
  },
  
  switchRole: (role, userId = null) =>
    AdvancedApiService.post('/role-switch/', { role, user_id: userId }),
}

// Personalization API
export const personalizationApi = {
  updatePreferences: (userId, preferences) =>
    AdvancedApiService.post('/personalization/', { user_id: userId, preferences }),
  
  getRecommendations: (userId) =>
    AdvancedApiService.post('/personalization/', { user_id: userId, action: 'get_recommendations' }),
}

// Multilingual API
export const multilingualApi = {
  detectLanguage: (text) =>
    AdvancedApiService.post('/multilingual/', { action: 'detect_language', text }),
  
  translateText: (text, sourceLang = 'auto', targetLang = 'en') =>
    AdvancedApiService.post('/multilingual/', { 
      action: 'translate', 
      text, 
      source_lang: sourceLang, 
      target_lang: targetLang 
    }),
  
  getGreeting: (language = 'en') =>
    AdvancedApiService.post('/multilingual/', { action: 'greeting', language }),
}

// Sustainability API
export const sustainabilityApi = {
  calculateEcoScore: (travelPlan) =>
    AdvancedApiService.post('/sustainability/', { action: 'eco_score', travel_plan: travelPlan }),
  
  getLocalArtisans: (location) =>
    AdvancedApiService.post('/sustainability/', { action: 'artisans', location }),
  
  getCarbonTips: (journeyType = 'pilgrimage') =>
    AdvancedApiService.post('/sustainability/', { action: 'carbon_tips', journey_type: journeyType }),
}

// Offline API
export const offlineApi = {
  getCachedData: () =>
    AdvancedApiService.get('/offline/'),
  
  getOfflineResponse: (query) =>
    AdvancedApiService.post('/offline/', { query }),
}

// Enhanced Meditation API
export const enhancedMeditationApi = {
  getPersonalizedRecommendations: (state, preferences = null) =>
    AdvancedApiService.post('/meditation/', { state, preferences }),
}

export default AdvancedApiService