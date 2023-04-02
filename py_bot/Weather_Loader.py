import requests
weather_api_key = "some api-key from openweather"
city = "Moscow"
class Weather:
    def __init__(self):
        self.data = ""
        self.city = ""
        self.temperature = ""
        self.feels_temperature = ""
        self.humidity = ""
        self.wind_speed = ""
    def get_weather(self):
        try:
            self.request = requests.get(
                f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric"
            )
            self.data = self.request.json()
            self.city = self.data['name']
            self.temperature = self.data['main']['temp']
            self.feels_temperature = self.data['main']['feels_like']
            self.humidity = self.data['main']['humidity']
            self.wind_speed = self.data['wind']['speed']
        except Exception as ex:
            print(ex)
