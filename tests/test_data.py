import unittest
import os
from datetime import datetime, date, timedelta
from redis import Redis
from app.data import LoadData, LoadMultipleData as LM

class TestData(unittest.TestCase):
    location = 'New Delhi'
    def test_data(self):
        
        LoadData.load_data(self.location)
        with Redis(host=os.environ['HOST'], port=os.environ['PORT'],
                   db=os.environ['DB'], password=os.environ['PASSWORD'],
                   decode_responses=True) as r:
            self.assertNotEqual(r.hgetall(f'{self.location}:{str(datetime.today().date())}'), {})

    def test_multiple_data(self):
        date1 = date.fromisoformat('2025-02-18')
        date2 = date.fromisoformat('2025-02-20')
        lm = LM(self.location, date1, date2)
        while date1 <= date2:
            with Redis(host=os.environ['HOST'], port=os.environ['PORT'],
                    db=os.environ['DB'], password=os.environ['PASSWORD'],
                    decode_responses=True) as r:
                self.assertIsNotNone(lm.get_item(self.location, date1))
            # print(f'type of date1: {type(date1)} \n type of timedelta {type(timedelta(days=1))}')                
            date1 += timedelta(days=1)
    
        