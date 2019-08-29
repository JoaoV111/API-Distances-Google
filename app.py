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

if __name__ == '__main__':
    app.run(debug=True)




