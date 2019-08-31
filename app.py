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
		Artist = request.form['artist']
		Title = request.form['title']
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

	if request.method == 'POST':
		f_id = resquest.form['f_id']
		s_id = resquest.form['s_id']
		
		try:
			url = f'https://joao-api-cryptocurrency.herokuapp.com/currency?f_id={f_id}&s_id={s_id}'
			req = requests.get(url)
			req_json = json.loads(req.text)
			result = ''
			div1 = req_json["div1"]
		except:
			result = 'No currencies found.'
		
		try:
			url = 'https://joao-api-cryptocurrency.herokuapp.com/currency/all'
			req_all = requests.get(url)
		except:
			result = 'Server error'

	return render_template('currency.html', result=result, div1=div1, req_all=req_all)

if __name__ == '__main__':
    app.run(debug=True)




