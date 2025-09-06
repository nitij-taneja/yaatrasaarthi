import React, { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card'
import { Button } from './ui/button'
import { Badge } from './ui/badge'
import { 
  Leaf, 
  Users, 
  TreePine, 
  Recycle, 
  Heart,
  MapPin,
  Phone,
  Star,
  Award,
  TrendingUp
} from 'lucide-react'
import { sustainabilityApi } from '../services/advancedApi'

const SustainabilityDashboard = () => {
  const [ecoScore, setEcoScore] = useState(null)
  const [localArtisans, setLocalArtisans] = useState([])
  const [carbonTips, setCarbonTips] = useState([])
  const [selectedLocation, setSelectedLocation] = useState('badrinath')
  const [travelPlan, setTravelPlan] = useState({
    transport: 'shared_vehicle',
    accommodation: 'homestay',
    plastic_free: true,
    local_food: true
  })

  useEffect(() => {
    loadSustainabilityData()
  }, [selectedLocation])

  const loadSustainabilityData = async () => {
    try {
      // Calculate eco score
      const scoreResponse = await sustainabilityApi.calculateEcoScore(travelPlan)
      setEcoScore(scoreResponse.eco_score)

      // Get local artisans
      const artisansResponse = await sustainabilityApi.getLocalArtisans(selectedLocation)
      setLocalArtisans(artisansResponse.artisans)

      // Get carbon tips
      const tipsResponse = await sustainabilityApi.getCarbonTips('pilgrimage')
      setCarbonTips(tipsResponse.tips)
    } catch (error) {
      console.error('Error loading sustainability data:', error)
    }
  }

  const updateTravelPlan = (key, value) => {
    const newPlan = { ...travelPlan, [key]: value }
    setTravelPlan(newPlan)
    
    // Recalculate eco score
    sustainabilityApi.calculateEcoScore(newPlan)
      .then(response => setEcoScore(response.eco_score))
      .catch(console.error)
  }

  const getScoreColor = (score) => {
    if (score >= 80) return 'text-green-600 bg-green-50'
    if (score >= 60) return 'text-yellow-600 bg-yellow-50'
    return 'text-red-600 bg-red-50'
  }

  const getScoreLabel = (score) => {
    if (score >= 80) return 'Excellent'
    if (score >= 60) return 'Good'
    return 'Needs Improvement'
  }

  return (
    <div className="space-y-6">
      {/* Eco Score Card */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Award className="w-5 h-5 text-green-600" />
            Your Eco-Impact Score
          </CardTitle>
          <CardDescription>
            Based on your travel choices and environmental impact
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-between mb-4">
            <div className="text-center">
              <div className={`text-4xl font-bold ${getScoreColor(ecoScore || 0)}`}>
                {ecoScore || 0}
              </div>
              <div className="text-sm text-gray-600">out of 100</div>
              <Badge className={getScoreColor(ecoScore || 0)}>
                {getScoreLabel(ecoScore || 0)}
              </Badge>
            </div>
            
            <div className="flex-1 ml-6">
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-sm">Transport Choice</span>
                  <select 
                    value={travelPlan.transport}
                    onChange={(e) => updateTravelPlan('transport', e.target.value)}
                    className="text-sm border rounded px-2 py-1"
                  >
                    <option value="public_transport">Public Transport (+20)</option>
                    <option value="shared_vehicle">Shared Vehicle (0)</option>
                    <option value="private_car">Private Car (-20)</option>
                  </select>
                </div>
                
                <div className="flex items-center justify-between">
                  <span className="text-sm">Accommodation</span>
                  <select 
                    value={travelPlan.accommodation}
                    onChange={(e) => updateTravelPlan('accommodation', e.target.value)}
                    className="text-sm border rounded px-2 py-1"
                  >
                    <option value="homestay">Homestay (+10)</option>
                    <option value="eco_hotel">Eco Hotel (+5)</option>
                    <option value="hotel">Regular Hotel (-15)</option>
                  </select>
                </div>
                
                <div className="flex items-center justify-between">
                  <span className="text-sm">Plastic-Free Travel</span>
                  <input
                    type="checkbox"
                    checked={travelPlan.plastic_free}
                    onChange={(e) => updateTravelPlan('plastic_free', e.target.checked)}
                    className="rounded"
                  />
                </div>
              </div>
            </div>
          </div>
          
          <div className="bg-green-50 p-3 rounded-lg">
            <div className="flex items-center gap-2 mb-2">
              <TrendingUp className="w-4 h-4 text-green-600" />
              <span className="font-medium text-green-800">Improvement Tips</span>
            </div>
            <ul className="text-sm text-green-700 space-y-1">
              <li>• Choose homestays to support local families</li>
              <li>• Use shared transport to reduce carbon footprint</li>
              <li>• Carry reusable water bottles and bags</li>
              <li>• Support local artisans and businesses</li>
            </ul>
          </div>
        </CardContent>
      </Card>

      {/* Local Artisans */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Users className="w-5 h-5 text-purple-600" />
            Support Local Artisans
          </CardTitle>
          <CardDescription>
            Connect with authentic craftspeople and support local communities
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="mb-4">
            <label className="text-sm font-medium">Select Location:</label>
            <select 
              value={selectedLocation}
              onChange={(e) => setSelectedLocation(e.target.value)}
              className="ml-2 border rounded px-3 py-1"
            >
              <option value="badrinath">Badrinath</option>
              <option value="kedarnath">Kedarnath</option>
              <option value="gangotri">Gangotri</option>
              <option value="yamunotri">Yamunotri</option>
            </select>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {localArtisans.length > 0 ? localArtisans.map((artisan, index) => (
              <div key={index} className="border rounded-lg p-4 hover:shadow-md transition-shadow">
                <div className="flex items-start justify-between mb-2">
                  <div>
                    <h4 className="font-semibold text-lg">{artisan.name}</h4>
                    <p className="text-purple-600 font-medium">{artisan.craft}</p>
                  </div>
                  <div className="flex items-center gap-1">
                    <Star className="w-4 h-4 text-yellow-500 fill-current" />
                    <span className="text-sm">4.8</span>
                  </div>
                </div>
                
                <p className="text-sm text-gray-600 mb-3">{artisan.specialty}</p>
                
                <div className="space-y-2">
                  <div className="flex items-center gap-2 text-sm">
                    <MapPin className="w-4 h-4 text-gray-500" />
                    <span>{artisan.location}</span>
                  </div>
                  <div className="flex items-center gap-2 text-sm">
                    <Phone className="w-4 h-4 text-gray-500" />
                    <span>{artisan.contact}</span>
                  </div>
                </div>
                
                <div className="mt-3 flex gap-2">
                  <Button size="sm" variant="outline" className="flex-1">
                    <Heart className="w-3 h-3 mr-1" />
                    Support
                  </Button>
                  <Button size="sm" className="flex-1">
                    Contact
                  </Button>
                </div>
              </div>
            )) : (
              <div className="col-span-2 text-center py-8 text-gray-500">
                <Users className="w-12 h-12 mx-auto mb-4 opacity-50" />
                <p>No artisans found for this location</p>
                <p className="text-sm">Check back later or try another destination</p>
              </div>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Carbon Footprint Tips */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <TreePine className="w-5 h-5 text-green-600" />
            Carbon Footprint Reduction
          </CardTitle>
          <CardDescription>
            Practical tips to minimize your environmental impact
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {carbonTips.map((tip, index) => (
              <div key={index} className="flex items-start gap-3 p-3 bg-green-50 rounded-lg">
                <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center flex-shrink-0">
                  <Leaf className="w-4 h-4 text-green-600" />
                </div>
                <div>
                  <p className="text-sm text-green-800">{tip}</p>
                </div>
              </div>
            ))}
          </div>
          
          <div className="mt-6 p-4 bg-blue-50 rounded-lg">
            <div className="flex items-center gap-2 mb-2">
              <Recycle className="w-5 h-5 text-blue-600" />
              <span className="font-medium text-blue-800">Did You Know?</span>
            </div>
            <p className="text-sm text-blue-700">
              Sustainable tourism can reduce environmental impact by up to 70% while supporting 
              local communities. Every eco-friendly choice you make helps preserve these sacred 
              places for future generations.
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

export default SustainabilityDashboard