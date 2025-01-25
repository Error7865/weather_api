from flask import request, jsonify
from . import api
from app.data import Data, MultipleData
from .error import bad_request

@api.get('/wr/<location>')
def day_weather(location):
    date = request.args.get('date')
    if date is None:
        d = Data(location)
    else:
        d = Data(location, date)
    return jsonify({
        'location' : d.full_location,
        # 'describe': d.desc,
        'minTemp': d.min_temp,
        'temp': d.temp,
        'maxTemp': d.max_temp,
        'rain': d.rain,
        'windgust': d.windgust,
        'windspeed': d.windspeed,
        'date': d.date, 
        'humidity': d.humidity
    })

@api.get('/hour/<location>/<date>')
def hour_weather(location, date):
    '''This one always looking for hour=? 
    value on url '''
    d = Data(location, date)
    hour = request.args.get('hour') or 0
    hours_data = d.get_hours()
    for item in hours_data:
        if item['datetime'].hour == int(hour):
            item['location'] = d.full_location
            return item
    return bad_request('Unvalid hour. Range 0-23')

@api.get('/days/<location>/<date1>/<date2>')
def days_weather(location, date1, date2):
    m = MultipleData(location, date1, date2)
    return jsonify(m.get_days_info())
    