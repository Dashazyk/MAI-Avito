from flask import Flask, request, abort
import requests
import json
import os
import grpc
import sys 

sys.path.append(os.path.split(os.path.realpath(sys.argv[0]))[0] + '/myauth')
print(sys.path)

import myauth.myauth_pb2 as ma
import myauth.myauth_pb2_grpc as ma_grpc

# import redis
# from redis.cluster import RedisCluster as Redis
from rediscluster import RedisCluster

# from datetime import datetime
import datetime

class WeatherServer():
    def __init__(self, url_template, api_key) -> None:
        api = Flask(__name__)

        self.api     = api
        self.url_t   = url_template
        self.api_key = api_key
        # self.myredis = Redis(host='redis-master-1', port=6373)
        startup_nodes = [
            {
                "host": "173.20.0.31",
                "port": "6373"
            },
            {
                "host": "173.20.0.32",
                "port": "6374"
            },
            {
                "host": "173.20.0.33",
                "port": "6375"
            },
            {
                "host": "173.20.0.34",
                "port": "6376"
            },
            {
                "host": "173.20.0.35",
                "port": "6377"
            },
            {
                "host": "173.20.0.36",
                "port": "6378"
            }
        ]
        self.myredis = RedisCluster(startup_nodes=startup_nodes, decode_responses=True)
        # self.myredis = redis.Redis(host='173.20.0.30', port=6379)

        @api.route('/', methods=['GET'])
        def first_page():
            return 'go to /weather'

        @api.route('/weather', methods=['GET'])
        def get_weather():
            print('== Getting weather ==')
            city = request.args.get('city', None)
            days = request.args.get('days', None)
            unam = request.headers.get('Own-Auth-UserName', None)

            if city:
                date = datetime.datetime.today() + datetime.timedelta(days=days if days else 0)
                print('getting from redis by:', str(city)+str(date))
                redised = None
                try:
                    redised = self.myredis.get(str(city)+str(date))
                except Exception as e:
                    print('E:', e)
                    
                if redised:
                    print('from redis')
                    return redised
                else:
                    print('from API')
                    return self.weather(city, days, unam)
            else:
                return {}
            
        @api.route('/weather', methods=['PUT'])
        def save_weather():
            print('== Saving weather ==')
            city = request.args.get('city', None)
            days = request.args.get('days', None)
            
            date = datetime.datetime.today() + datetime.timedelta(days=days if days else 0)

            unam = request.headers.get('Own-Auth-UserName', None)
            self.myredis.set(str(city)+str(date), request.data)
            print('saving to redis by:', str(city)+str(date))
            return self.weather(city, days, unam)
            # city = request.args.get('city', None)
            # days = request.args.get('days', None)
            # unam = request.headers.get('Own-Auth-UserName', None)
            # if city:
            #     return self.weather(city, days, unam)
            # else:
            #     return {}
            
        
    def run(self):
        self.api.run(host='0.0.0.0', port = os.environ.get('WEATHER_PORT', 8080))

    def weather(self, city, days, username):
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = ma_grpc.AuthCheckerStub(channel)
            response = stub.CheckAuth(ma.AuthRequest(name=username))
            print("can view: " + str(response.can_view))

        if response.can_view:
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
                temp_c   = last_day['avgtemp_c']

            return {
                'city': city,
                'unit': 'celsius',
                'temperature':int(temp_c)
            }
        else:
            abort(403)

        
if __name__ == '__main__':
    weatherapi_key = '946cb665ad7f482ba68165257232703'
    # url = 'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m'
    url = 'http://api.weatherapi.com/v1/forecast.json?key={key}&q={city}&days={days}&aqi=no&alerts=no'
    
    # print(request_url)

    weather_server = WeatherServer(url, weatherapi_key)
    weather_server.run()


