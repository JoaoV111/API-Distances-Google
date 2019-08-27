from flask import Flask, render_template
from urllib.request import Request, urlopen

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
	
@app.route("/music-lyrics/")
def MusicLyrics():
	request = Request('https://api.lyrics.ovh/v1/slipknot/before i forget')
	response_body = urlopen(request).read()
	return render_template('musiclyrics.html')



