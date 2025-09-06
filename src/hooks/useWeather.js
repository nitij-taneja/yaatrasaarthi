import { useState, useCallback } from 'react'
import { weatherApi } from '../services/api'

export const useWeather = () => {
  const [weather, setWeather] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState(null)

  const getWeather = useCallback(async (location) => {
    if (!location) return

    setIsLoading(true)
    setError(null)

    try {
      const data = await weatherApi.getWeather(location)
      setWeather(data)
      return data
    } catch (err) {
      setError('Failed to fetch weather data')
      console.error('Weather fetch error:', err)
      throw err
    } finally {
      setIsLoading(false)
    }
  }, [])

  const clearWeather = useCallback(() => {
    setWeather(null)
    setError(null)
  }, [])

  return {
    weather,
    isLoading,
    error,
    getWeather,
    clearWeather
  }
}