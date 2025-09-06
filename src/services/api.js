const API_BASE_URL = 'http://localhost:8000/api'

class ApiService {
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

  static async get(endpoint) {
    return this.request(endpoint, { method: 'GET' })
  }

  static async post(endpoint, data) {
    return this.request(endpoint, {
      method: 'POST',
      body: JSON.stringify(data),
    })
  }

  static async put(endpoint, data) {
    return this.request(endpoint, {
      method: 'PUT',
      body: JSON.stringify(data),
    })
  }

  static async delete(endpoint) {
    return this.request(endpoint, { method: 'DELETE' })
  }
}

// Chat API
export const chatApi = {
  sendMessage: (message, sessionId = null, context = {}) =>
    ApiService.post('/chat/', { message, session_id: sessionId, context }),
  
  getSession: (sessionId) =>
    ApiService.get(`/sessions/${sessionId}/`),
    
  getSessionMessages: (sessionId) =>
    ApiService.get(`/sessions/${sessionId}/messages/`),
}

// Weather API
export const weatherApi = {
  getWeather: (location) =>
    ApiService.post('/weather/', { location }),
    
  getWeatherByLocation: (location) =>
    ApiService.get(`/weather/${location}/`),
}

// Destinations API
export const destinationsApi = {
  getAll: () => ApiService.get('/destinations/'),
  getById: (id) => ApiService.get(`/destinations/${id}/`),
}

// Eco Tips API
export const ecoTipsApi = {
  getAll: () => ApiService.get('/eco-tips/'),
  getById: (id) => ApiService.get(`/eco-tips/${id}/`),
}

// Meditation API
export const meditationApi = {
  getRecommendations: (state) =>
    ApiService.post('/meditation/', { state }),
}

// Local Artisans API
export const artisansApi = {
  getAll: () => ApiService.get('/artisans/'),
  getById: (id) => ApiService.get(`/artisans/${id}/`),
}

export default ApiService