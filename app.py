from flask import Flask, render_template
import requests
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/music-lyrics/')
def MusicLyrics():
	request = requests.get('https://api.lyrics.ovh/v1/Coldplay/Adventure of a Lifetime')
	lyrics_json = json.loads(request.text)
	lyrics = lyrics_json["lyrics"]
	lyrics = lyrics.replace("\n","<br/>")
	return render_template('musiclyrics.html', lyrics=lyrics)

if __name__ == '__main__':
    app.run(debug=True)




