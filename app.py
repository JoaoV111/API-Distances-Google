from flask import Flask, render_template, request
import requests
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/music-lyrics/', methods=['POST', 'GET'])
def MusicLyrics():
	lyrics = ''
	Artist = 'artist'
	Title = 'title'
	if request.method == 'POST':
		Artist = request.form['artist'].strip()
		Title = request.form['title'].strip()
		try:
			url = f'https://api.lyrics.ovh/v1/{Artist}/{Title}'
			req = requests.get(url)
			lyrics_json = json.loads(req.text)
			lyrics = lyrics_json["lyrics"]
			lyrics = lyrics.replace("\n","<br>")
		except:
			lyrics = 'No lyrics found.', 404
	
	return render_template('musiclyrics.html', lyrics=lyrics, Artist=Artist, Title=Title)

@app.route('/crypto-currency/', methods=['POST', 'GET'])
def CryptoCurrency():
	result = ''
	req_json = [{},{}]
	f_value = 1.0

	if request.method == 'POST':
		f_name = request.form['f_name'].strip().capitalize()
		s_name = request.form['s_name'].strip().capitalize()
		f_value = str(request.form['f_value']).replace(',', '.')
		
		
		try:
			url = 'https://joao-api-cryptocurrency.herokuapp.com/currency/all'
			req_all = requests.get(url)
			req_json_all = json.loads(req_all.text)
			f_id = ''
			s_id = ''
			for currency in req_json_all:
				if currency['name'].lower() == f_name.lower():
					f_id = currency['id']
				if currency['name'].lower() == s_name.lower():
					s_id = currency['id']
			url = (f'https://joao-api-cryptocurrency.herokuapp.com/currency'
				   f'?f_id={f_id}&s_id={s_id}&f_value={f_value}')	
			req = requests.get(url)
			req_json = json.loads(req.text)
			if req.status_code != 200:
				req_json = [{},{}]
				result = 'Currencies not found.', 404
		except:
			result = 'Server Error.', 500
	
	return render_template('currency.html', result=result, req_json=req_json, f_value=f_value)

if __name__ == '__main__':
    app.run(debug=True)




