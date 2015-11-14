import json
from flask import Flask
import urllib.request
import pandas as pd



app = Flask(__name__)

cities = {'amsterdam': '6544881',
'berlin': '5245497',
'dublin': '2964574',
'helsinki': '658225',
'london': '2643741',
'madrid': '3117735',
}

API_KEY = 'afeab278b59f85b0a0305ab7d5dbb968'

def fetch_weather():
    city_ids = ','.join(cities.values())
    url = 'http://api.openweathermap.org/data/2.5/group?id=%s&APPID=%s' % (city_ids, API_KEY)
    response = urllib.request.urlopen(url)
    str_response = response.readall().decode('utf-8')
    data = json.loads(str_response)
    filtered_data = [(x['name'], x['main']['temp']) for x in data['list']]

    weather_df = pd.DataFrame.from_dict(filtered_data)
    weather_df.columns = ['Name', 'Temperature']
    return weather_df

def transform_kelvin_to_celsius(weather_df):
    conversion_list = [ 273.15 ] * len(weather_df)
    weather_df['Temperature'] = weather_df['Temperature'].subtract(conversion_list)
    return weather_df


def get_max_weather(weather_df):
    max_temp_row = weather_df['Temperature'].argmax()
    max_temp_city = weather_df.ix[max_temp_row, 'Name']
    max_temp = weather_df.ix[max_temp_row, 'Temperature']
    return (max_temp_city, max_temp)

def get_min_weather(weather_df):
    min_temp_row = weather_df['Temperature'].argmin()
    min_temp_city = weather_df.ix[min_temp_row, 'Name']
    min_temp = weather_df.ix[min_temp_row, 'Temperature']
    return (min_temp_city, min_temp)

@app.route('/')
def index():
    return 'Hello! Welcome to the temperature city calculator'

@app.route('/warmest_city/')
def warmest_city():
    weather_df = fetch_weather()
    weather_df = transform_kelvin_to_celsius(weather_df)
    (max_temp_city, max_temp) = get_max_weather(weather_df)
    return '%s, %s' % (max_temp_city, max_temp)

@app.route('/coldest_city/')
def coldest_city():
    weather_df = fetch_weather()
    weather_df = transform_kelvin_to_celsius(weather_df)
    (min_temp_city, min_temp) = get_min_weather(weather_df)
    return '%s, %s' % (min_temp_city, min_temp)

if __name__ == '__main__':
    app.run()