import React from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card'
import { Button } from './ui/button'
import { Cloud, Thermometer, Droplets, Wind, Loader2 } from 'lucide-react'
import { useWeather } from '../hooks/useWeather'

const WeatherWidget = ({ destinations = [] }) => {
  const { weather, isLoading, error, getWeather } = useWeather()

  const handleGetWeather = async (locationName) => {
    try {
      await getWeather(locationName)
    } catch (error) {
      console.error('Weather fetch failed:', error)
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Cloud className="w-5 h-5 text-blue-500" />
          Weather Information
        </CardTitle>
        <CardDescription>
          Get current weather for Char Dham destinations
        </CardDescription>
      </CardHeader>
      
      <CardContent>
        {/* Destination Buttons */}
        <div className="grid grid-cols-2 gap-2 mb-6">
          {destinations.map((destination) => (
            <Button
              key={destination.id}
              variant="outline"
              size="sm"
              onClick={() => handleGetWeather(destination.name)}
              disabled={isLoading}
              className="text-xs"
            >
              {destination.name}
            </Button>
          ))}
        </div>

        {/* Loading State */}
        {isLoading && (
          <div className="flex items-center justify-center py-8">
            <div className="flex items-center gap-2">
              <Loader2 className="w-5 h-5 animate-spin text-blue-500" />
              <span className="text-sm text-gray-600">Fetching weather data...</span>
            </div>
          </div>
        )}

        {/* Error State */}
        {error && (
          <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
            <p className="text-sm text-red-600">{error}</p>
          </div>
        )}

        {/* Weather Data */}
        {weather && !isLoading && (
          <div className="bg-gradient-to-br from-blue-50 to-indigo-50 p-4 rounded-lg border">
            <h3 className="font-semibold text-lg mb-3 text-gray-800">
              {weather.location}
            </h3>
            
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-3">
                <div className="flex items-center gap-2">
                  <Thermometer className="w-4 h-4 text-red-500" />
                  <div>
                    <p className="text-sm text-gray-600">Temperature</p>
                    <p className="font-semibold">{weather.temperature}°C</p>
                  </div>
                </div>
                
                <div className="flex items-center gap-2">
                  <Cloud className="w-4 h-4 text-gray-500" />
                  <div>
                    <p className="text-sm text-gray-600">Condition</p>
                    <p className="font-semibold capitalize">{weather.description}</p>
                  </div>
                </div>
              </div>
              
              <div className="space-y-3">
                <div className="flex items-center gap-2">
                  <Droplets className="w-4 h-4 text-blue-500" />
                  <div>
                    <p className="text-sm text-gray-600">Humidity</p>
                    <p className="font-semibold">{weather.humidity}%</p>
                  </div>
                </div>
                
                <div className="flex items-center gap-2">
                  <Wind className="w-4 h-4 text-green-500" />
                  <div>
                    <p className="text-sm text-gray-600">Wind Speed</p>
                    <p className="font-semibold">{weather.wind_speed} m/s</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Default State */}
        {!weather && !isLoading && !error && (
          <div className="text-center py-8">
            <Cloud className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <p className="text-gray-500">Click on a destination to get weather information</p>
          </div>
        )}
      </CardContent>
    </Card>
  )
}

export default WeatherWidget