from flask import Flask, request
import requests
import json
import os

class WeatherServer():
    def __init__(self, url_template, api_key) -> None:
        api = Flask(__name__)

        self.api = api
        self.url_t = url_template
        self.api_key = api_key

        @api.route('/', methods=['GET'])
        def first_page():
            return 'hello, my little penguineee'

        @api.route('/weather', methods=['GET'])
        def weather():
            city = request.args.get('city', None)
            days = request.args.get('days', None)
            if city:
                return self.weather(city, days)
            else:
                return {}
            
        
    def run(self):
        self.api.run(host='0.0.0.0', port = os.environ.get('WEATHER_PORT', 8080))

    def weather(self, city, days):
        request_url = url.format(
            key = weatherapi_key, 
            city = city,
            days = days
        )

        response = requests.get(request_url)
        j_sponse = json.loads(response.text)

        if not days:
            temp_c = j_sponse['current']['temp_c']
        else:
            last_day = j_sponse['forecast']['forecastday'][-1]['day']
            temp_c = last_day['avgtemp_c']

        return {
            'city': city,
            'unit': 'celsius',
            'temperature':int(temp_c)
        }

        
if __name__ == '__main__':
    weatherapi_key = '946cb665ad7f482ba68165257232703'
    # url = 'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m'
    url = 'http://api.weatherapi.com/v1/forecast.json?key={key}&q={city}&days={days}&aqi=no&alerts=no'
    
    # print(request_url)

    weather_server = WeatherServer(url, weatherapi_key)
    weather_server.run()


