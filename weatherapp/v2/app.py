from pyowm import OWM
from flask import Flask, render_template, request
from flask_wtf.csrf import CSRFProtect
from pyzipcode import ZipCodeDatabase
import db as dynamodb
import os
import sys

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
    zipcode = zcdb[zip_code]
    city = zipcode.city
    state = zipcode.state
    country = 'US'
    return f"{city}, {state}, {country}"

def santize(location):
    location = location.split(',')
      
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
    return render_template('500.html')

@app.route('/')
def home():
    return render_template('weather.html')

@app.route('/weather', methods=['POST'])
def weather():
    location = request.form['city']
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
    print(weather, file=sys.stderr)
    response = dynamodb.write_to_weather(weather['location'],weather['current'],weather['ftemp'],weather['ctemp'])
    print(response, file=sys.stderr)
    if (response['ResponseMetadata']['HTTPStatusCode'] != 200):
        return render_template('error.html', message="Failed to save weather data to DynamoDB.")
    return response 