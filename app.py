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
		if Artist == '' or Title == '':
			Artist = 'artist'
			Title = 'title'
		try:
			url = f'https://api.lyrics.ovh/v1/{Artist}/{Title}'
			req = requests.get(url)
			lyrics_json = json.loads(req.text)
			lyrics = lyrics_json["lyrics"]
			lyrics = lyrics.replace("\n","<br>")
		except:
			lyrics = 'No lyrics found.'
	
	return render_template('musiclyrics.html', lyrics=lyrics, Artist=Artist, Title=Title)

@app.route('/crypto-currency/', methods=['POST', 'GET'])
def CryptoCurrency():
	f_id = ''
	s_id = ''
	f_name = ''
	s_name = ''
	result = ''
	req_json = [{},{}]

	if request.method == 'POST':
		f_name = request.form['f_name'].strip().capitalize()
		s_name = request.form['s_name'].strip().capitalize()
		
		try:
			url = 'https://joao-api-cryptocurrency.herokuapp.com/currency/all'
			req_all = requests.get(url)
			req_json_all = json.loads(req_all.text)
			for currency in req_json_all:
				if currency['name'].lower() == f_name.lower():
					f_id = currency['id']
				if currency['name'].lower() == s_name.lower():
					s_id = currency['id']
			url = f'https://joao-api-cryptocurrency.herokuapp.com/currency?f_id={f_id}&s_id={s_id}'
			req = requests.get(url)
			req_json = json.loads(req.text)
			if req_json == [{}]:
				req_json = [{},{}]
				result = 'Currencies not found.'
		except:
			result = 'Server Error.'
		
	return render_template('currency.html', result=result, f_name=f_name, s_name=s_name,
	                       req_json=req_json)

if __name__ == '__main__':
    app.run(debug=True)




