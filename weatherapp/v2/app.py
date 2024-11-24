from pyowm import OWM
from flask import Flask, render_template, request
from flask_wtf.csrf import CSRFProtect
from pyzipcode import ZipCodeDatabase
import db as dynamodb
import os


SECRET_KEY = os.urandom(32)
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
csrf = CSRFProtect(app)
owm = OWM(os.environ['API'])
zcdb = ZipCodeDatabase()
mgr = owm.weather_manager()

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html')

@app.route('/')
def home():
    return render_template('weather.html')

@app.route('/weather', methods=['POST'])
def weather():
    location = request.form.get('city')
    if not location:
        raise ValueError("No location was provided. Please enter a valid ZIP code or City, State, Country.")
    try:
        if location.isdigit() and len(location) == 5:
            try:
                zipcode = zcdb[location]
                city = zipcode.city
                state = zipcode.state
                country = 'US'
            except KeyError:
                raise ValueError("Invalid ZIP code provided.")
        else:
            breakdown = location.split(',')
            if len(breakdown) < 1:
                raise ValueError("Invalid input format. Use ZIP code or City, State, Country.")
            city = breakdown[0].strip()
            state = breakdown[1].strip() if len(breakdown) > 1 else ''
            country = breakdown[2].strip() if len(breakdown) > 2 else 'US'

        city_weather = f"{city},{state},{country}"
        observation = mgr.weather_at_place(city_weather)
        w = observation.weather

        ftemp = w.temperature(unit='fahrenheit')['temp']
        ctemp = w.temperature(unit='celsius')['temp']
        descript = w.detailed_status
        icon_code = w.weather_icon_name
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        weather = {
            'location': city,
            'current': descript,
            'ftemp': int(ftemp),
            'ctemp': int(ctemp),
            'icon_url': icon_url 
        }

        add_weather(weather)
        return render_template("city.html", weather=weather)

    except ValueError as ve:
        return render_template('error.html', error=str(ve))
    except Exception as e:
        return render_template('error.html', error=str(e))
      
def add_weather(weather):
    response = dynamodb.write_to_weather(weather['location'],weather['current'],(int(weather['ftemp'])),(int(weather['ctemp'])))
    if (response['ResponseMetadata']['HTTPStatusCode'] == 200):
        return {
            'msg': 'Added successfully',
        }
    return {  
        'msg': 'Some error occcured',
        'response': response
    }
