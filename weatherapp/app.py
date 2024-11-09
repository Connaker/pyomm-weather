
from pyowm import OWM
from pyowm.commons.exceptions import NotFoundError
from flask import Flask, render_template, request, jsonify
from flask_wtf.csrf import CSRFProtect
from pyzipcode import ZipCodeDatabase
import ast
import os

SECRET_KEY = os.urandom(32)
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
csrf = CSRFProtect(app)
owm = OWM(os.environ['API'])

@app.route('/')
def index():
    return render_template('weather.html')

@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html")

@app.route('/search', methods=['POST'])
def search():
    weather = {}
    search = request.form['response']
    if search == '':
        e = 'Field cannot be blank'
        return render_template('invalid.html', error=e)
    n = ast.literal_eval(search)
    if isinstance(n,int):
        if len(str(n)) == 5:
            zcdb = ZipCodeDatabase()
            city = zcdb[n].city
            state = zcdb[n].state
            place = city+','+state+','+"US"
            weather.update({
                    'zipcode': n,
                    'city': city,
                    'state': state,
                    'place': place,
            })
        else:
            e = 'Field is invalid Zip'
            return render_template('invalid.html', error=e)
    if place is None:
        place = search
        weather.update ({
            'location': place,
        })
    mgr = owm.weather_manager()
    observation = mgr.weather_at_place(place)
    w = observation.weather
    ftemp = w.temperature(unit='fahrenheit')['temp']
    ctemp = w.temperature(unit='celsius')['temp']
    descript = w.detailed_status
    weather.update ({
        'current': descript,
        'ftemp': ftemp,
        'ctemp': ctemp,
    })
    return render_template("zip.html", weather=weather)