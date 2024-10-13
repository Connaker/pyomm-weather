
from pyowm import OWM 
from pyowm.commons.exceptions import NotFoundError
from flask import Flask, render_template, request
from pyzipcode import ZipCodeDatabase
import ast



app = Flask(__name__)
owm = OWM("8f535614e6c42132a9290ce12a4e5e69")

@app.route('/')
def index():
    return render_template('weather.html')

@app.route('/search', methods=['POST'])
def search():
    search = request.form['response']
    if search == '':
        e = 'Field cannot be blank'
        return render_template('invalid.html', error=e) 
    n = eval(search)
    if type(n) == int:
            if len(str(n)) == 5:
                 zcdb = ZipCodeDatabase()
                 city = zcdb[n].city
                 state = zcdb[n].state
                 place = city+','+state+','+"US"
                 mgr=owm.weather_manager()
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
                # e = 'Field is valid Zip'
                # return render_template('invalid.html', error=e)
            else:
                e = 'Field is invalid Zip'
                return render_template('invalid.html', error=e)
    else:
        # loc = str(n)
        # e = loc
        try:
            location = ast.literal_eval(search)
            mgr=owm.weather_manager()
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
        
        except NotFoundError:
             e = search,'+','not in regsitry. Please check your input'
             return render_template("invalid.html",error=e)
         
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)