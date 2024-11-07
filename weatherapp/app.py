
from pyowm import OWM
from pyowm.commons.exceptions import NotFoundError
from flask import Flask, render_template, request, jsonify
from flask_wtf.csrf import CSRFProtect
from pyzipcode import ZipCodeDatabase
import ast
import os


def create_app():
    csrf = CSRFProtect(app)
    app = Flask(__name__)
    owm = OWM(os.environ['API'])
    csrf.init_app(app)
    SECRET_KEY = os.urandom(32)
    app.config['SECRET_KEY'] = SECRET_KEY


    @app.route('/')
    def index():
        return render_template('weather.html')

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template("500.html")

    @app.route('/search', methods=['POST'])
    def search():
        search = request.form['response']
        # if search == '':
        #     e = 'Field cannot be blank'
        #     return render_template('invalid.html', error=e)
        n = eval(search)
        if type(n) == int:
            if len(str(n)) == 5:
                zcdb = ZipCodeDatabase()
                city = zcdb[n].city
                state = zcdb[n].state
                place = city+','+state+','+"US"
                mgr = owm.weather_manager()
                observation = mgr.weather_at_place(place)
                w = observation.weather
                ftemp = w.temperature(unit='fahrenheit')['temp']
                ctemp = w.temperature(unit='celsius')['temp']
                descript = w.detailed_status

                weather = {
                    'zipcode': n,
                    'current': descript,
                    'city': city,
                    'state': state,
                    'place': place,
                    'ftemp': ftemp,
                    'ctemp': ctemp,
                }
                return render_template("zip.html", weather=weather)
            else:
                e = 'Field is invalid Zip'
                return render_template('invalid.html', error=e)
        elif type(n) != int:
            location = ast.literal_eval(search)
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


        #     try:

        #         location = ast.literal_eval(search)
        #         mgr = owm.weather_manager()
        #         observation = mgr.weather_at_place(location)
        #         w = observation.weather
        #         ftemp = w.temperature(unit='fahrenheit')['temp']
        #         ctemp = w.temperature(unit='celsius')['temp']
        #         descript = w.detailed_status
        #         weather = {
        #             'location': location,
        #             'current': descript,
        #             'ftemp': ftemp,
        #             'ctemp': ctemp,
        #         }
        #         return render_template("city.html", weather=weather)

        #     except:
        #         e = "Something went wrong."
        #         return render_template("invalid.html", error=e)
        # else:
        #     e = "Something went wrong."
        #     return render_template("invalid.html", error=e)
            
