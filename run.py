import json
from flask import Flask, render_template
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
    '''Pulls data for European capitals from OpenWeatherMap. Returns a pandas DataFrame
    with the temperature results.
    returns: pd.DataFrame, 'Name' and 'Temperature' columns
    '''
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
    '''
    Given some pandas dataframe with name and temperature columns,
    transforms the temperature column from Kelvin to Celsius.
    args: weather_df: pd Dataframe with 'Name' and 'Temperature' columns
        returns: pd Dataframe with 'Name' and 'Temperature' columns
    '''
    conversion_list = [ 273.15 ] * len(weather_df)
    weather_df['Temperature'] = weather_df['Temperature'].subtract(conversion_list)
    return weather_df


def get_max_weather(weather_df):
    '''
    Given some pandas dataframe with name and temperature columns,
    returns a two-value tuple with the highest temperature identified
    in the df, as well as its corresponding city name.
    Args: weather_df: pd Dataframe with 'Name' and 'Temperature' columns
        returns: (max_temp_city: str, max_temp: float)
    '''
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
    return render_template('index.html')

@app.route('/warmest_city/')
def warmest_city():
    weather_df = fetch_weather()
    weather_df = transform_kelvin_to_celsius(weather_df)
    (max_temp_city, max_temp) = get_max_weather(weather_df)
    context = {'city_name': max_temp_city,
                'temp': str(max_temp)}
    return render_template('base_city_temp.html', context=context)

@app.route('/coldest_city/')
def coldest_city():
    weather_df = fetch_weather()
    weather_df = transform_kelvin_to_celsius(weather_df)
    (min_temp_city, min_temp) = get_min_weather(weather_df)
    context = {'city_name': min_temp_city,
                'temp': min_temp}
    return render_template('base_city_temp.html', context=context)


if __name__ == '__main__':
    app.run()