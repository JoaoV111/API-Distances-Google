from app import app
import unittest
import requests
from unittest import mock

class Test(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()

    def test_request(self):
        result = self.app.get('/')
        self.assertEqual(result.status_code, 200) 
        result = self.app.get('/music-lyrics/')
        self.assertEqual(result.status_code, 200)
        result = self.app.get('/crypto-currency/')
        self.assertEqual(result.status_code, 200)

class Test_response:
    def fetch_json(self, url):
        response = requests.get(url)
        return response.json()

def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if args[0] == 'https://joao-api-cryptocurrency.herokuapp.com/currency/all':
        return MockResponse({"key1": "value1"}, 200)
    elif args[0] == 'https://joao-api-cryptocurrency.herokuapp.com/currency?f_id=bitcoin&s_id=iota&f_value=1.0':
        return MockResponse({"key2": "value2"}, 200)

    return MockResponse(None, 404)

class Test_API(unittest.TestCase):

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_fetch(self, mock_get):

        tr = Test_response()
        json_data = tr.fetch_json('https://joao-api-cryptocurrency.herokuapp.com/currency/all')
        self.assertEqual(json_data, {"key1": "value1"})
        json_data = tr.fetch_json('https://joao-api-cryptocurrency.herokuapp.com/currency?'
                                  'f_id=bitcoin&s_id=iota&f_value=1.0')
        self.assertEqual(json_data, {"key2": "value2"})
        json_data = tr.fetch_json('http://whatever.com/whatever.json')
        self.assertIsNone(json_data)

        self.assertIn(mock.call('https://joao-api-cryptocurrency.herokuapp.com/currency/all'), mock_get.call_args_list)
        self.assertIn(mock.call('https://joao-api-cryptocurrency.herokuapp.com/currency?'
                                'f_id=bitcoin&s_id=iota&f_value=1.0'), mock_get.call_args_list)

        self.assertEqual(len(mock_get.call_args_list), 3)


if __name__ == "__main__":
    print ('Strating Tests')
    print('----------------------------------------------------------------------')
    unittest.main(verbosity=2)