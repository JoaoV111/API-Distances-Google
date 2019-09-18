from app import app
import unittest
import requests
from unittest import mock

def mocked_requests_get(*args, **kwargs):
    # mock request setup
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.status_code = status_code
            self.text = json_data

    if args[0] == 'https://joao-api-cryptocurrency.herokuapp.com/currency/all':
        return MockResponse('''[{
                                "id": "bitcoin", 
                                "name": "Bitcoin", 
                                "symbol": "btc"
                                },
                                {
                                "id": "iota", 
                                "name": "IOTA", 
                                "symbol": "miota"
                                }]''', 200)
    elif args[0] == 'https://joao-api-cryptocurrency.herokuapp.com/currency?f_id=bitcoin&s_id=iota&f_value=1.0':
        return MockResponse('''[
                                {
                                "id": "bitcoin", 
                                "name": "Bitcoin", 
                                "price": 10377.16, 
                                "value": 1.0
                                }, 
                                {
                                "id": "iota", 
                                "name": "IOTA", 
                                "price": 0.236409, 
                                "value": 43894.94477790609
                                }
                                ]''', 200)
    elif args[0] == 'https://api.lyrics.ovh/v1/The Beatles/Her Majesty':
        return MockResponse('''{"lyrics": "Her Majesty's a pretty nice girl"
                                }''', 200)

    return MockResponse(None, 404)

class Tests(unittest.TestCase):
        
    def setUp(self):
        # create instance of unittest
        self.app = app.test_client()

    def test_request(self):
        # test all urls requests 
        result = self.app.get('/')
        self.assertEqual(result.status_code, 200) 
        result = self.app.get('/music-lyrics/')
        self.assertEqual(result.status_code, 200)
        result = self.app.get('/crypto-currency/')
        self.assertEqual(result.status_code, 200)

    @mock.patch('app.requests.get', side_effect=mocked_requests_get)
    def test_API_Cryptocurrency(self, mock_get):
        # test API cryptocurrency response
        result = self.app.post('/crypto-currency/', 
                               data={ "f_name": "bitcoin", "s_name": "iota", "f_value": 1.0 }, 
                               content_type= 'application/x-www-form-urlencoded')
        self.assertEqual(result.status_code, 200)
        self.assertIn('Bitcoin'.encode(), result.data)
        self.assertIn('IOTA'.encode(), result.data)
        self.assertIn('10377.16'.encode(), result.data)
        self.assertIn('0.236409'.encode(), result.data)
        self.assertIn('43894.94477790609'.encode(), result.data)

    @mock.patch('app.requests.get', side_effect=mocked_requests_get)
    def test_API_MusicLyrics(self, mock_get):
        # test API MusicLyrics
        result = self.app.post('/music-lyrics/', 
                               data={ 'artist': 'The Beatles', 'title': 'Her Majesty' }, 
                               content_type= 'application/x-www-form-urlencoded')
        self.assertEqual(result.status_code, 200)
        self.assertIn('The Beatles'.encode(), result.data)
        self.assertIn('Her Majesty'.encode(), result.data)
        lyrics = ("Her Majesty's a pretty nice girl".encode())
        self.assertIn(lyrics, result.data)

if __name__ == "__main__":
    print ('Strating Tests')
    print('----------------------------------------------------------------------')
    unittest.main(verbosity=2)
