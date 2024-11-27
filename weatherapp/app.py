from pyowm import OWM
from flask import Flask, render_template, request
from flask_wtf.csrf import CSRFProtect
from pyzipcode import ZipCodeDatabase
import ast
import os


"""
    This program retrives the weather based on a Zipcode, City and Country or City, State and Country.

    This program is broken into 3 functions
                                                                                                        !
    internal_server_error: Renders 500 error page if program recieves a 500 error handler
    index: Renders the weather.html
    search: Retrieves POST data from weather.html form. Gets Location from Zip code and weather from
             the location.
"""

SECRET_KEY = os.urandom(32)
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
csrf = CSRFProtect(app)
owm = OWM(os.environ['API'])

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html')

@app.route('/')
def index():
    return render_template('weather.html')


@app.route('/search', methods=['POST'])
def search():

    """
        Function recieves the location from form.
        Runs through basic IF to verify variable has data
        Second IF verifies if it is a Zipcode. If it is, uses pyzipcode to retrieve City, State.
        Lastly, gathers weather information from location using pyowm.
        Renders data to city.html
    """

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
            location = city+','+state+','+"US"
        else:
            e = 'Field is invalid Zip'
            return render_template('invalid.html', error=e)
    else:
            location = n

    mgr = owm.weather_manager()
    observation = mgr.weather_at_place(location)
    w = observation.weather
    ftemp = w.temperature(unit='fahrenheit')['temp']
    ctemp = w.temperature(unit='celsius')['temp']
    descript = w.detailed_status
    weather = {
            'location': location,
            'current': descript,
            'ftemp': ftemp,
            'ctemp': ctemp,
    }
    return render_template("city.html", weather=weather)