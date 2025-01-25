import json
import requests
import os
from datetime import datetime

class Data:
    def __init__(self, location, \
                date1 = f'{datetime.now().year}-{datetime.now().month}-{datetime.now().day}'):
        url = os.environ.get('URL')+os.environ.get('API_KEY')
        url = url.replace('[location]', location)
        url = url.replace('[date1]', date1)
        res = requests.get(url=url)
        data = json.loads(res.text)
        self.full_location = data['resolvedAddress']
        self.location = data['address']
        # self.desc = data['description']
        self.__hour = data['days'][0]['hours']
        days_data = data['days'][0]
        self.temp = days_data['temp']
        self.max_temp = days_data['tempmax']
        self.min_temp = days_data['tempmin']
        self.rain = days_data['snow']
        self.windgust = days_data['windgust']
        self.windspeed = days_data['windspeed']
        self.pressure = days_data['pressure']
        self.uv = days_data['uvindex']
        self.icon = days_data['icon']
        self.humidity = days_data['humidity']
        self.date = days_data['datetime']

    def get_hours(self) -> list:
        '''It will return list of data base on hours'''
        hours = []
        for day in self.__hour:
            # print(day['datetime'])
            value = {}
            value['datetime'] = datetime.strptime(f'{self.date} {day['datetime']}', \
                                r'%Y-%m-%d %H:%M:%S')
            value['temp'] = day['temp']
            value['humidity'] = day['humidity']
            value['snow'] = day['snow']
            value['wind'] = day['windspeed']
            value['uv'] = day['uvindex']
            value['pressure'] = day['pressure']
            hours.append(value)
        return hours

    def get_hour_info(self, hour:int):
        '''This will return a particular hour info of
        a day.'''
        for item in self.get_hours():
            if item['datetime'].hour == hour:
                return item
        return None



class MultipleData:
    def __init__(self, location:str, date1:str, date2:str):
        '''date1 and date2 was two different date it format will be
        yyyy-mm-dd'''
        url = os.environ.get('URL1')+os.environ.get('API_KEY')
        url = url.replace('[location]', location)
        url = url.replace('[date1]', date1)
        url = url.replace('[date2]', date2)
        res = requests.get(url=url)
        data = json.loads(res.text)     #catching data
        self.location = data['resolvedAddress']
        self.desc = data['description']
        self.__data = data['days']

    def decorate_days_info(self, day:dict)->dict:
        info = dict()
        info['datetime'] = datetime.strptime(day['datetime'], r'%Y-%m-%d')
        info['tempmax'] = day['tempmax']
        info['temp'] = day['temp']
        info['tempmin'] = day['tempmin']
        info['humidity'] = day['humidity']
        info['snow'] = day['snow']
        info['uv'] = day['uvindex']
        info['windspeed'] = day['windspeed']
        info['windgust'] = day['windgust']
        info['pressure'] = day['pressure']
        return info

    def get_days_info(self)->list:
        days = {}
        days['day'] = list()
        for item in self.__data:
            days['day'].append(self.decorate_days_info(item))
        return days
    