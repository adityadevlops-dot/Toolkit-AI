"""
Weather Tool - Get current weather information.
Uses FREE APIs - No API key required!
"""

import requests
from typing import Optional
from .base_tool import BaseTool


class WeatherTool(BaseTool):
    """Get current weather for any location using free APIs."""
    
    def __init__(self):
        super().__init__()
        self.name = "weather"
        self.description = "Get current weather information for any city or location. Returns temperature, conditions, humidity, and wind speed. No API key required."
        
        self.parameters = {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City name (e.g., 'London', 'New York', 'Tokyo', 'Mumbai')"
                },
                "units": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"],
                    "description": "Temperature units (default: celsius)",
                    "default": "celsius"
                }
            },
            "required": ["location"]
        }
    
    def execute(self, location: str, units: str = "celsius") -> str:
        """Get weather for location."""
        
        location = location.strip()
        
        if not location:
            return "❌ Please provide a location (e.g., 'London' or 'New York')"
        
        # Try multiple APIs in order
        result = self._try_wttr_in(location, units)
        
        if result is None:
            result = self._try_open_meteo(location, units)
        
        if result is None:
            return f"❌ Could not get weather for '{location}'. Please check the city name and try again."
        
        return result
    
    def _try_wttr_in(self, location: str, units: str) -> Optional[str]:
        """Try wttr.in API (free, no key needed)."""
        try:
            # Format URL - wttr.in is very flexible with location names
            url = f"https://wttr.in/{location}?format=j1"
            
            headers = {
                'User-Agent': 'curl/7.68.0',
                'Accept': 'application/json'
            }
            
            response = requests.get(url, headers=headers, timeout=15)
            
            if response.status_code != 200:
                return None
            
            data = response.json()
            
            # Check if we got valid data
            if 'current_condition' not in data or not data['current_condition']:
                return None
            
            current = data['current_condition'][0]
            
            # Get location info
            if 'nearest_area' in data and data['nearest_area']:
                area = data['nearest_area'][0]
                city = area.get('areaName', [{}])[0].get('value', location)
                country = area.get('country', [{}])[0].get('value', '')
                location_str = f"{city}, {country}" if country else city
            else:
                location_str = location
            
            # Get temperature based on units
            if units == "fahrenheit":
                temp = current.get('temp_F', 'N/A')
                feels_like = current.get('FeelsLikeF', 'N/A')
                temp_unit = "°F"
            else:
                temp = current.get('temp_C', 'N/A')
                feels_like = current.get('FeelsLikeC', 'N/A')
                temp_unit = "°C"
            
            # Get other weather info
            weather_desc = current.get('weatherDesc', [{}])[0].get('value', 'Unknown')
            humidity = current.get('humidity', 'N/A')
            wind_speed = current.get('windspeedKmph', 'N/A')
            wind_dir = current.get('winddir16Point', '')
            visibility = current.get('visibility', 'N/A')
            uv_index = current.get('uvIndex', 'N/A')
            
            # Get weather emoji
            emoji = self._get_weather_emoji(weather_desc)
            
            return f"""🌍 **Weather in {location_str}** {emoji}

🌡️ **Temperature:** {temp}{temp_unit}
🤔 **Feels Like:** {feels_like}{temp_unit}
☁️ **Conditions:** {weather_desc}
💧 **Humidity:** {humidity}%
💨 **Wind:** {wind_speed} km/h {wind_dir}
👁️ **Visibility:** {visibility} km
☀️ **UV Index:** {uv_index}"""

        except requests.exceptions.Timeout:
            return None
        except requests.exceptions.ConnectionError:
            return None
        except Exception:
            return None
    
    def _try_open_meteo(self, location: str, units: str) -> Optional[str]:
        """Try Open-Meteo API (free, no key needed)."""
        try:
            # Step 1: Get coordinates from location name
            geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={location}&count=1&language=en"
            
            geo_response = requests.get(geo_url, timeout=10)
            geo_data = geo_response.json()
            
            if not geo_data.get('results'):
                return None
            
            result = geo_data['results'][0]
            lat = result['latitude']
            lon = result['longitude']
            city = result.get('name', location)
            country = result.get('country', '')
            location_str = f"{city}, {country}" if country else city
            
            # Step 2: Get weather data
            temp_unit_param = "fahrenheit" if units == "fahrenheit" else "celsius"
            
            weather_url = (
                f"https://api.open-meteo.com/v1/forecast?"
                f"latitude={lat}&longitude={lon}"
                f"&current_weather=true"
                f"&temperature_unit={temp_unit_param}"
            )
            
            weather_response = requests.get(weather_url, timeout=10)
            weather_data = weather_response.json()
            
            if 'current_weather' not in weather_data:
                return None
            
            current = weather_data['current_weather']
            
            temp = current.get('temperature', 'N/A')
            temp_unit = "°F" if units == "fahrenheit" else "°C"
            wind_speed = current.get('windspeed', 'N/A')
            wind_dir = self._degrees_to_direction(current.get('winddirection', 0))
            weather_code = current.get('weathercode', 0)
            weather_desc = self._weather_code_to_description(weather_code)
            emoji = self._get_weather_emoji(weather_desc)
            
            return f"""🌍 **Weather in {location_str}** {emoji}

🌡️ **Temperature:** {temp}{temp_unit}
☁️ **Conditions:** {weather_desc}
💨 **Wind:** {wind_speed} km/h {wind_dir}

📍 *Data from Open-Meteo*"""

        except Exception:
            return None
    
    def _get_weather_emoji(self, description: str) -> str:
        """Get weather emoji based on description."""
        desc = description.lower()
        
        if any(word in desc for word in ['sun', 'clear', 'fine']):
            return '☀️'
        elif any(word in desc for word in ['partly', 'partial']):
            return '⛅'
        elif any(word in desc for word in ['cloud', 'overcast']):
            return '☁️'
        elif any(word in desc for word in ['rain', 'drizzle', 'shower']):
            return '🌧️'
        elif any(word in desc for word in ['thunder', 'storm', 'lightning']):
            return '⛈️'
        elif any(word in desc for word in ['snow', 'flurr', 'blizzard']):
            return '❄️'
        elif any(word in desc for word in ['fog', 'mist', 'haze']):
            return '🌫️'
        elif any(word in desc for word in ['wind', 'gust']):
            return '💨'
        else:
            return '🌤️'
    
    def _degrees_to_direction(self, degrees: float) -> str:
        """Convert wind degrees to compass direction."""
        directions = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE',
                      'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
        index = round(degrees / 22.5) % 16
        return directions[index]
    
    def _weather_code_to_description(self, code: int) -> str:
        """Convert WMO weather code to description."""
        codes = {
            0: 'Clear sky',
            1: 'Mainly clear',
            2: 'Partly cloudy',
            3: 'Overcast',
            45: 'Foggy',
            48: 'Depositing rime fog',
            51: 'Light drizzle',
            53: 'Moderate drizzle',
            55: 'Dense drizzle',
            61: 'Slight rain',
            63: 'Moderate rain',
            65: 'Heavy rain',
            71: 'Slight snow',
            73: 'Moderate snow',
            75: 'Heavy snow',
            77: 'Snow grains',
            80: 'Slight rain showers',
            81: 'Moderate rain showers',
            82: 'Violent rain showers',
            85: 'Slight snow showers',
            86: 'Heavy snow showers',
            95: 'Thunderstorm',
            96: 'Thunderstorm with slight hail',
            99: 'Thunderstorm with heavy hail',
        }
        return codes.get(code, 'Unknown')