import os
import httpx
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
LAT = os.getenv("CITY_LAT")
LON = os.getenv("CITY_LON")

async def get_current_weather_details() -> dict:
    """
    Fetches ambient temperature and precipitation status from OpenWeather API.
    Provides explicit error output inside the terminal for debugging purposes.
    """
    if not API_KEY:
        print("Log: OPENWEATHER_API_KEY is missing from the configuration environment.")
        return None
        
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LON}&appid={API_KEY}&units=metric"
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=5.0)
            
            if response.status_code == 200:
                data = response.json()
                temp = data.get("main", {}).get("temp", 0)
                
                weather_list = data.get("weather", [])
                is_raining = False
                
                if weather_list:
                    main_weather = weather_list[0].get("main", "").lower()
                    if "rain" in main_weather or "thunderstorm" in main_weather or "drizzle" in main_weather:
                        is_raining = True
                        
                return {"temp": temp, "is_raining": is_raining}
            else:
                print(f"Error: Weather API returned status code {response.status_code}")
                print(f"Server response payload: {response.text}")
                return None
                
        except httpx.RequestError as req_err:
            print(f"Network error executing weather request parameters: {req_err}")
            return None
        except Exception as e:
            print(f"Unexpected error encountered inside the weather evaluation engine: {e}")
            return None
