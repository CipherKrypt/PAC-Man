"""
Contains API Classes for different use cases
Each class has functions that can be called that interact with different 
Publicly available APIs and return the result.

"""
import os
from dotenv import load_dotenv
import requests, json

# Loading environment variables from the .env file
load_dotenv()
# Accessing the API key for weather
weather = os.getenv("WEATHER")
open = os.getenv("OPEN")

# A timeIt decorator to know how long each function takes to execute
def timeIt(func, *args, **kwargs):
    import time
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Function '{func.__name__}' executed in {elapsed_time} seconds")
        return result
    return wrapper

# This function will use the API provided by 'weatherapi.com' to give user the weather report of the given city
# @timeIt
def get_weather(city:str)->str: # takes  a city name as input and returns the current weather as string
    from math import ceil, floor
    API_key = open #weather
    lat,lon = (25.3573, 55.4033)
    # base_url variable to store url
    url = f"api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_key}"
    # base_url = "https://api.weatherapi.com/v1/forecast.json"
    # # complete url address
    # complete_url = base_url + "?key=" + api_key + "&q=" + city.title() + "&aqi=no"

    # return response object
    forecast_response = requests.get(url)
    Forecast = forecast_response.json()
    # print(forecast)

    if Forecast.get('error') == None:

        current = Forecast.get('current')
        forecast = Forecast.get('forecast')['forecastday'][0]['day']

        current_temperature = int(current["temp_c"])
        feels_like = ceil(current["feelslike_c"])
        min_temperature = floor(forecast["mintemp_c"])
        max_temperature = ceil(forecast["maxtemp_c"])
        current_humidity = current["humidity"]
        rain_chance = forecast['daily_chance_of_rain']
        weather_description = current['condition']['text']
        print(current_temperature, feels_like, min_temperature, max_temperature, current_humidity , weather_description)

        # print following values
        weather_report = f"""Current Temperature is {current_temperature} degrees Celsius. But it feels like {feels_like} degrees Celsius.
Forecast for today recorded as, 
Minimum temperature being {min_temperature} degrees Celsius. And Maximum temperature being {max_temperature} degrees Celsius.
The Humidity is {current_humidity} percent.
And the chance of rain is at {rain_chance} percent.
Weather Description: {weather_description}."""

    if __name__ == "__main__":
        print(weather_report)
    else:
        return weather_report


if __name__ == "__main__":
    get_weather('Sharjah')
    print()

      

        
    