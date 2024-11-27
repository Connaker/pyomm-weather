from pyowm import OWM
from flask import Flask, render_template, request
from flask_wtf.csrf import CSRFProtect
from pyzipcode import ZipCodeDatabase
import db as dynamodb
import os
import sys


"""
    This program retrives the weather based on a Zipcode, City and Country or City, State and Country.

    This program is broken into 8 functions

    generate_secret_key: Generates a random key for the CSRFProtect
    get_weather: Retrieves the weather from a specified location
    get_location: Takes the Zip code and identifies the city and state, returns City, State and Country 
                  (US)
    santize: This santizes variations of how data is entered in the form box (City,State,Country, City, 
             State, Country, City,State, Country, etc) so that it will always be City, State, Country or 
             City, Country.
    internal_server_error: Renders 500 error page if program recieves a 500 error handler
    home: Renders the weather.html
    weather: Retrieves POST data from weather.html form. Uses get_weather, get_location functions to retrieve 
             weather and location from zip code. Sends data to add_weather function and to city.html
    add_weather: Collects data sent from weather function, uses db.py to send the data to DynamoDB
"""

app = Flask(__name__)
app.secret_key = os.urandom(24).hex()
csrf = CSRFProtect(app)
owm = OWM(os.environ['API'])
zcdb = ZipCodeDatabase()
mgr = owm.weather_manager()
error = 'error.html'

def generate_secret_key():
    return os.urandom(24).hex()
app.secret_key = generate_secret_key()

def get_weather(location):

    """
        Function retrieves the weather.
        Try/except used to identify any Exception errors. Using pyowm library and API key, function
        retrieves the weather data and returns it as ftemp, ctemp, icon_url and descript.
    """

    try: 
        observation = mgr.weather_at_place(location)
        w = observation.weather
        ftemp = w.temperature(unit='fahrenheit')['temp']
        ctemp = w.temperature(unit='celsius')['temp']
        descript = w.detailed_status
        icon_code = w.weather_icon_name
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        return ftemp, ctemp, icon_url, descript
    except Exception:
        return None, None, None, None 
    
def get_location(zip_code):

    """
                                                                                                                !
        Function retrieves the location.
        Using the pyzipcode library, retrieves the city and state for the zipcode entered and returns it as
        city, state and country.
    """
    # Transforms zip code to City and State using the pyzipcode Library.
    zipcode = zcdb[zip_code]
    city = zipcode.city
    state = zipcode.state
    country = 'US'
    return f"{city}, {state}, {country}"

def santize(location):
    location = location.split(',')
  
    """
        Function santizes the location.
        Using IF statements, identifies if the data is 3 words or 2 words and santizes the data format
        to be the same and returns it as location.
    """

    if len(location) == 2:
        return f"{location[0].strip()}, {location[1].strip()}"
    
    if len(location) >= 3:
        formatted_location = [location[0].strip()]
        formatted_location.append(f" {location[1].strip()}")
        formatted_location.append(f" {location[2].strip()}")

        if len(location) > 3:
            formatted_location.extend(location[3:])
        return ','.join(formatted_location)
    return location

@app.errorhandler(500)
def internal_server_error(e):

    # Renders 500 error page if program recieves a 500 error handler
    return render_template('500.html')

@app.route('/')
def home():
    return render_template('weather.html')

@app.route('/weather', methods=['POST'])
def weather():
    location = request.form['city']

    """
        Function recieves the city from form.
        Try/except used to identify any ValueError or Exception errors. If statement in Try identifies if the
        recieved data is digits and if so, uses get_location to convert to location. Secondary Try/Get sends 
        data to get_location to retrieve location and identifies any KeyErrors. Otherwise, the location recieved 
        is santized. Then it retrieves the ftemp, ctemp, icon_url, descript from the get_weather function.        
        Finally data is is collected in a dictionary and sent to the add weather function and to the city.html.   
    """
    try:
        if location.isdigit() and len(location) == 5:
            try:
                location = get_location(location)
            except KeyError:
                    raise ValueError("Invalid ZIP code provided.")
        location=santize(location)
        ftemp, ctemp, icon_url, descript = get_weather(location)
        weather = {
                'location': location,
                'current': descript,
                'ftemp': int(ftemp),
                'ctemp': int(ctemp),
                'icon_url': icon_url 
            }
        add_weather(weather)
        return render_template("city.html", weather=weather)
    except ValueError as ve:
        return render_template(error, error=str(ve))
    except Exception as e:
        return render_template(error, error=str(e))

def add_weather(weather):

    """
        Function sends the weather information to DynamoDB.
        Simple function that uses the db.py to send the data to DynamoDB. If statement renders errors to error.html
        Print statements used for debug and outputs to stderr.
    """
    
    print(weather, file=sys.stderr)
    response = dynamodb.write_to_weather(weather['location'],weather['current'],weather['ftemp'],weather['ctemp'])
    print(response, file=sys.stderr)
    if (response['ResponseMetadata']['HTTPStatusCode'] != 200):
        return render_template('error.html', message="Failed to save weather data to DynamoDB.")
    return response 