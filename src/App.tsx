import React, { useState, useEffect } from 'react'
import { Button } from './components/ui/button'
import { Input } from './components/ui/input'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './components/ui/card'
import { Badge } from './components/ui/badge'
import { Tabs, TabsContent, TabsList, TabsTrigger } from './components/ui/tabs'
import { MessageCircle, MapPin, Cloud, Heart, Leaf, Users, Send, Loader2, Sparkles, Award } from 'lucide-react'
import AdvancedChatInterface from './components/AdvancedChatInterface'
import SustainabilityDashboard from './components/SustainabilityDashboard'
import WeatherWidget from './components/WeatherWidget'

function App() {
  const [destinations, setDestinations] = useState([])
  const [ecoTips, setEcoTips] = useState([])
  const [artisans, setArtisans] = useState([])
  const [isLoading, setIsLoading] = useState(true)

  const API_BASE_URL = 'http://localhost:8000/api'

  useEffect(() => {
    loadInitialData()
  }, [])

  const loadInitialData = async () => {
    setIsLoading(true)
    try {
      await Promise.all([
        loadDestinations(),
        loadEcoTips(),
        loadArtisans()
      ])
    } catch (error) {
      console.error('Error loading initial data:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const loadDestinations = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/destinations/`)
      if (response.ok) {
        const data = await response.json()
        setDestinations(data)
      }
    } catch (error) {
      console.error('Error loading destinations:', error)
    }
  }

  const loadEcoTips = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/eco-tips/`)
      if (response.ok) {
        const data = await response.json()
        setEcoTips(data)
      }
    } catch (error) {
      console.error('Error loading eco tips:', error)
    }
  }

  const loadArtisans = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/artisans/`)
      if (response.ok) {
        const data = await response.json()
        setArtisans(data)
      }
    } catch (error) {
      console.error('Error loading artisans:', error)
    }
  }

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-orange-50 to-blue-50 flex items-center justify-center">
        <div className="text-center">
          <Loader2 className="w-12 h-12 animate-spin text-orange-600 mx-auto mb-4" />
          <p className="text-lg text-gray-600">Loading YatraSaarthi...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-50 to-blue-50">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-5xl font-bold text-orange-800 mb-4 flex items-center justify-center gap-3">
            🕉️ YatraSaarthi
          </h1>
          <p className="text-xl text-gray-700 max-w-2xl mx-auto">
            Your Spiritual Travel Companion for India's Sacred Destinations
          </p>
          <p className="text-sm text-gray-600 mt-2">
            Discover the divine journey through Char Dham with AI-powered guidance
          </p>
        </div>

        <Tabs defaultValue="chat" className="w-full">
          <TabsList className="grid w-full grid-cols-6 mb-8">
            <TabsTrigger value="chat" className="flex items-center gap-2">
              <MessageCircle className="w-4 h-4" />
              AI Chat
            </TabsTrigger>
            <TabsTrigger value="destinations" className="flex items-center gap-2">
              <MapPin className="w-4 h-4" />
              Destinations
            </TabsTrigger>
            <TabsTrigger value="weather" className="flex items-center gap-2">
              <Cloud className="w-4 h-4" />
              Weather
            </TabsTrigger>
            <TabsTrigger value="eco-tips" className="flex items-center gap-2">
              <Leaf className="w-4 h-4" />
              Eco Tips
            </TabsTrigger>
            <TabsTrigger value="artisans" className="flex items-center gap-2">
              <Users className="w-4 h-4" />
              Artisans
            </TabsTrigger>
            <TabsTrigger value="sustainability" className="flex items-center gap-2">
              <Award className="w-4 h-4" />
              Sustainability
            </TabsTrigger>
          </TabsList>

          {/* Chat Tab */}
          <TabsContent value="chat">
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <div className="lg:col-span-2">
                <AdvancedChatInterface userId="demo_user_123" />
              </div>
              <div className="space-y-4">
                <Card>
                  <CardHeader>
                    <CardTitle className="text-lg flex items-center gap-2">
                      <Sparkles className="w-5 h-5 text-orange-500" />
                      AI Features
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-2">
                    <div className="text-sm text-gray-600 mb-3">
                      Experience advanced AI with:
                    </div>
                    <div className="space-y-2 text-sm">
                      <div className="flex items-center gap-2">
                        <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                        <span>🧠 LLM-powered responses</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                        <span>🔍 RAG knowledge retrieval</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <div className="w-2 h-2 bg-purple-500 rounded-full"></div>
                        <span>🌍 Multilingual support</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <div className="w-2 h-2 bg-orange-500 rounded-full"></div>
                        <span>🎤 Voice interaction</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <div className="w-2 h-2 bg-red-500 rounded-full"></div>
                        <span>🎭 Dynamic role switching</span>
                      </div>
                    </div>
                    
                    <div className="pt-3 border-t">
                      <Button variant="outline" className="w-full justify-start text-sm">
                      <MapPin className="w-4 h-4 mr-2" />
                      Switch to Travel Planner
                    </Button>
                    <Button variant="outline" className="w-full justify-start text-sm">
                      <Cloud className="w-4 h-4 mr-2" />
                      Ask about Weather
                    </Button>
                    <Button variant="outline" className="w-full justify-start text-sm">
                      <Heart className="w-4 h-4 mr-2" />
                      Get Meditation Guide
                    </Button>
                    <Button variant="outline" className="w-full justify-start text-sm">
                      <Leaf className="w-4 h-4 mr-2" />
                      Learn Eco Tips
                    </Button>
                    </div>
                  </CardContent>
                </Card>
              </div>
            </div>
          </TabsContent>

          {/* Destinations Tab */}
          <TabsContent value="destinations">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {destinations.length > 0 ? destinations.map((destination) => (
                <Card key={destination.id} className="hover:shadow-lg transition-shadow">
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <MapPin className="w-5 h-5 text-orange-500" />
                      {destination.name}
                    </CardTitle>
                    <CardDescription className="flex items-center gap-2">
                      <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded-full text-xs">
                        {destination.altitude}
                      </span>
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <p className="mb-4 text-gray-700">{destination.description}</p>
                    <div className="space-y-3">
                      <div>
                        <strong className="text-orange-700">Best Time:</strong>
                        <span className="ml-2">{destination.best_time}</span>
                      </div>
                      <div>
                        <strong className="text-orange-700">Mythology:</strong>
                        <p className="mt-1 text-sm text-gray-600">{destination.mythology}</p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              )) : (
                <Card className="col-span-2">
                  <CardContent className="p-8 text-center">
                    <MapPin className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                    <p className="text-gray-500">Loading destinations...</p>
                  </CardContent>
                </Card>
              )}
            </div>
          </TabsContent>

          {/* Weather Tab */}
          <TabsContent value="weather">
            <WeatherWidget destinations={destinations} />
          </TabsContent>

          {/* Eco Tips Tab */}
          <TabsContent value="eco-tips">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {ecoTips.length > 0 ? ecoTips.map((tip) => (
                <Card key={tip.id} className="hover:shadow-md transition-shadow">
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2 text-lg">
                      <Leaf className="w-5 h-5 text-green-500" />
                      {tip.title}
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p className="text-gray-700 mb-3">{tip.description}</p>
                    <Badge variant="outline" className="bg-green-50 text-green-700 border-green-200">
                      {tip.category}
                    </Badge>
                  </CardContent>
                </Card>
              )) : (
                <Card className="col-span-3">
                  <CardContent className="p-8 text-center">
                    <Leaf className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                    <p className="text-gray-500">Loading eco-friendly tips...</p>
                  </CardContent>
                </Card>
              )}
            </div>
          </TabsContent>

          {/* Artisans Tab */}
          <TabsContent value="artisans">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {artisans.length > 0 ? artisans.map((artisan) => (
                <Card key={artisan.id} className="hover:shadow-lg transition-shadow">
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <Users className="w-5 h-5 text-purple-500" />
                      {artisan.name}
                    </CardTitle>
                    <CardDescription>{artisan.craft_type}</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      <div>
                        <strong className="text-purple-700">Location:</strong>
                        <span className="ml-2">{artisan.location}</span>
                      </div>
                      <p className="text-gray-700">{artisan.description}</p>
                      <div className="bg-purple-50 p-3 rounded-lg">
                        <strong className="text-purple-700">Contact:</strong>
                        <p className="text-sm mt-1">{artisan.contact_info}</p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              )) : (
                <Card className="col-span-3">
                  <CardContent className="p-8 text-center">
                    <Users className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                    <p className="text-gray-500">Loading local artisans...</p>
                  </CardContent>
                </Card>
              )}
            </div>
          </TabsContent>

          {/* Sustainability Tab */}
          <TabsContent value="sustainability">
            <SustainabilityDashboard />
          </TabsContent>
        </Tabs>

        {/* Footer */}
        <div className="mt-12 text-center text-gray-600">
          <p className="text-sm">
            🙏 Namaste! Experience the divine journey with YatraSaarthi - Your advanced AI spiritual travel companion with LLM, RAG, multilingual support, and voice interaction
          </p>
        </div>
      </div>
    </div>
  )
}

export default App