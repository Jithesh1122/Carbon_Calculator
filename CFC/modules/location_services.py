import requests
import os
from dotenv import load_dotenv

load_dotenv()

class LocationServices:
    def __init__(self):
        self.api_key = os.getenv("OPENAQ_API_KEY")

    def get_air_quality(self, lat, lon):
        url = f"https://api.openaq.org/v2/latest?coordinates={lat},{lon}&key={self.api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            aqi = data['results'][0]['measurements'][0]['value']
            return {"aqi": aqi, "status": self.get_aqi_status(aqi)}
        return None

    def get_aqi_status(self, aqi):
        if aqi <= 50:
            return "Good"
        elif aqi <= 100:
            return "Moderate"
        elif aqi <= 150:
            return "Unhealthy for Sensitive Groups"
        elif aqi <= 200:
            return "Unhealthy"
        elif aqi <= 300:
            return "Very Unhealthy"
        else:
            return "Hazardous"
