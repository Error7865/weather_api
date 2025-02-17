from flask import request, jsonify
from datetime import datetime, date, timedelta
from . import api
from app.data import LoadData, LoadMultipleData
from .error import bad_request
from app import r, limiter

@api.get('/wr/<location>')
@limiter.limit('20 per day')
def day_weather(location):
    res = LoadData.load_data(location)
    if res is not None:
        return bad_request(res.text)
    data = r.hgetall(f'{location}:{str(datetime.today().date())}')
    # if d.error is None:
    return jsonify({
        'location' : data['resolvedAddress'],
        # 'describe': d.desc,
        'minTemp': data['tempmin'],
        'temp': data['temp'],
        'maxTemp': data['tempmax'],
        'rain': data['snow'],
        'windgust': data['windgust'],
        'windspeed': data['windspeed'],
        'date': data['datetime'], 
        'humidity': data['humidity']
    })
    # return bad_request('Unvalid city code.')

@api.get('/hour/<location>/<date>')
@limiter.limit('48/day')
def hour_weather(location, date):
    '''This one always looking for hour=? 
    value on url '''
    hour = request.args.get('hour') or 0
    hour = int(hour)
    if hour < 0 or hour > 23:
        return bad_request('Unvalid hour. Range 0-23')
    res = LoadData.load_data(location, date)
    if res is not None:
        return bad_request(res.text)
    data = dict()
    data = r.hgetall(f'{location}:{date}:{str(hour).zfill(2)}')
    return jsonify(data)
    
@api.get('/multiple/<location>/<date1>/<date2>')
@limiter.limit('10/day;1/hour')
def multiple_day(location, date1, date2):
    date1 = date.fromisoformat(date1)      
    date2 = date.fromisoformat(date2)       #converting str to date object
    if not date1 < date2:
        return bad_request('Check dates wisely.')
    lm = LoadMultipleData(location, date1, date2)
    days_data_ls = list()       # will hold days data
    while date1 <= date2:
        days_data_ls.append(lm.get_item(location, date1))
        date1 += timedelta(days=1)
    return jsonify({
        'days': days_data_ls
    })


#Testing limiter
@api.route('/slow')
@limiter.limit('1 per day')
def slow():
    return ":("