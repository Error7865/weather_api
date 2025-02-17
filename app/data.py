import requests
import os
from datetime import datetime, date, timedelta
from app import r

class LoadData:
    def __init__(self):
        pass

    def has_key(self, key:str)->bool:
        '''will check that key exists or not and 
        return boolean value'''
        if r.exists(key) == 1:
            return True
        return False


    @staticmethod
    def load_data(location:str, date1=str(datetime.today().date())):
        l = LoadData()
        if not l.has_key(f'{location}:{date1}'):
            try:
                data, sub_data = l.get(location, date1) 
            except ValueError:
                res = l.get(location, date1)
                return res          #return result if anything wrong happen.
            r.hset(f'{location}:{date1}', mapping=data)
            r.expire(f'{location}:{date1}', 24*60*60, nx = True)
            for key in list(sub_data.keys()):
                r.hset(f'{location}:{date1}:{key}', mapping=sub_data[key])
                r.expire(f'{location}:{date1}:{key}', 24*60*60, nx = True)
        # else:
        #     print('Data already exists.')
        return None

    def is_plain_data(self, value)->bool:
        '''It will check data types dic/list or not
        if not present return `True`
        else return `False` '''
        types = [type([]), type({})] #thoes are type which was differen from raw type(int, float, str)
        #present on weather response data
        if type(value) not in types:
            return True
        return False

    def get_plain_dict(self, dic: dict)-> set:
        '''This method will return plain dict and skip 
        thoes are contain list or dictionary
        return data differnt keys
        `data` that desire for 
        `different_keys`  are hold list or dict'''
        data = {}
        for key in list(dic.keys()):
            if self.is_plain_data(dic[key]) \
                and dic[key] is not None:
                data[key] = dic[key]
        return data

    def get(self, location, \
                date2 = f'{datetime.now().year}-{datetime.now().month}-{datetime.now().day}'):
        data = {}
        # types = [type([]), type({})] #thoes are type which was differen from raw type(int, float, str)
        #present on weather response data
        differen_keys = list() # it will store thoes key which are hold
#dict or list datatypes
        url = os.environ.get('URL')+os.environ.get('API_KEY')
        url = url.replace('[location]', location)
        url = url.replace('[date1]', str(date2))
        res = requests.get(url=url)
        if res.status_code != 200:
            return res          #return result if anything wrong happen.
        raw_data = res.json()
        for key in list(raw_data):
            if self.is_plain_data(raw_data[key]):
                data[key] = raw_data[key]
            else:
                differen_keys.append(key)
        sub_data = {}
        for key in differen_keys:
            if key == 'days':   #operation for `days` key
                data.update(self.get_plain_dict(raw_data[key][0])) 
                sub_data.update(self.__hours_operation(raw_data[key][0]['hours']))
        return data, sub_data
        
    def __hours_operation(self, hour_data:list):
        '''This method will adjust data base on hours'''
        data = dict()
        for item in hour_data:
            key = item['datetime'].split(':')[0]
            for sub_key in list(item.keys()):
                if item[sub_key] is not None and \
                    self.is_plain_data(item[sub_key]):
                        try: 
                            data[key][sub_key] = item[sub_key]
                        except KeyError as e:
                            data[key] = {}
                            data[key][sub_key] = item[sub_key]
        return data

    def get_item(self, location:str, date1:str):
        '''This will return data from redis'''
        if self.has_key(f'{location}:{date1}'):
            return r.hgetall(f'{location}:{date1}')
        return None


class LoadMultipleData(LoadData):
    def __init__(self, location:str, date1:str, date2:str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # date1 = date.fromisoformat(date1)
        # date2 = date.fromisoformat(date2)
        while date1 <= date2:
            self.load_to_redis(location, date1)
            date1 += timedelta(days=1)
           
        # return None
    def load_to_redis(self, location, date1):
        if not self.has_key(f'{location}:{date1}'):
            try:
                data, sub_data = self.get(location, date1) 
            except ValueError:
                res = self.get(location, date1)
                return res          #return result if anything wrong happen.
            r.hset(f'{location}:{date1}', mapping=data)
            r.expire(f'{location}:{date1}', 24*60*60, nx = True)
            for key in list(sub_data.keys()):
                r.hset(f'{location}:{date1}:{key}', mapping=sub_data[key])
                r.expire(f'{location}:{date1}:{key}', 24*60*60, nx = True)