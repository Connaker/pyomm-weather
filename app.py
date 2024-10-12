import pyowm
import geocoder
import re
from flask import Flask, flash, redirect, render_template, request, session
from pyzipcode import ZipCodeDatabase
from geopy.geocoders import Nominatim



app = Flask(__name__)

owm = pyowm.OWM('8f535614e6c42132a9290ce12a4e5e69')
mgr=owm.weather_manager()



@app.route('/', methods=['GET', 'POST'])
def home():
    location = geocoder.ip('me').latlng
    my_lat = location[0]
    my_lon = location[1]

    lat = [float(my_lat)]
    lon = [float(my_lon)]
    coordinates = str(my_lat)+", "+str(my_lon)
    geolocator = Nominatim(user_agent="mcflaskweatherapp")
    location = geolocator.reverse(coordinates)
    address = location.raw['address']
    city = address.get('town')
    state = address.get('state')

    observation = mgr.weather_at_coords(my_lat,my_lon)
    w = observation.weather
    ftemp = w.temperature(unit='fahrenheit')['temp']
    ctemp = w.temperature(unit='celsius')['temp']
    condition = w.status

    weather = {
        'lat': lat,
        'lon': lon,
        'city': city,
        'state': state,
        'ftemp': ftemp,
        'ctemp': ctemp,
        'condition': condition,
    }
    print(city)

    return render_template("weather.html", weather=weather)

@app.route('/zip', methods=['GET', 'POST'])
def zip():
    # Zip Code
    if request.method == "GET":
        return render_template("weather.html")

    if request.method == "POST":
        if not request.form.get("zipcode"):
            return render_template("invalid.html")
        zipcode = request.form.get("zipcode")

        if len(str(zipcode)) > 5:
            return render_template("invalid.html")

        if len(str(zipcode)) <= 1:
            return render_template("invalid.html")
        
        zcdb = ZipCodeDatabase()
        city = zcdb[zipcode].city
        state = zcdb[zipcode].state
        place = city+','+state
        observation = mgr.weather_at_place('place')
        w = observation.weather
        ftemp = w.temperature(unit='fahrenheit')['temp']
        ctemp = w.temperature(unit='celsius')['temp']

        weather = {
        'zipcode': zipcode,
        'city': city,
        'state': state,
        'place': place,
        'ftemp': ftemp,
        'ctemp': ctemp,
        }
        return render_template("zip.html", weather=weather)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
