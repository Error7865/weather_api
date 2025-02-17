import unittest
from app import create_app

class TestAPI(unittest.TestCase):
    location = 'memari'
    def setUp(self):
        app = create_app('test')
        self.app_context = app.app_context()
        self.app_context.push()
        self.client = app.test_client()

    def tearDown(self):
        self.app_context.pop()

    def test_day_weather(self):
        url = f'api/wr/{self.location}'
        res = self.client.get(url)
        # print(res.text)
        self.assertIn('humidity', res.text)
        self.assertIn('temp', res.text)

    def test_hour_weather(self):
        url = f'api/hour/{self.location}/2025-01-22'
        res = self.client.get(url+'?hour=12')
        self.assertIn('12', res.text)
        self.assertIn('humidity', res.text)

        #getting bad request error
        res = self.client.get(url+'?hour=25')
        self.assertEqual(res.status_code, 400)
        self.assertIn('Unvalid hour', res.text) 
