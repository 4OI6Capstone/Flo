from flask import Flask
from flask import request
import mutagen

app = Flask(__name__)


@app.route("/get-mix", methods=['POST'])
def getmix():
    song_list = request.files.getlist("files")
    for file in song_list:
        song = mutagen.File(file, easy=True)
        artist = song.get('artist')
        title = song.get('title')
        album = song.get('album')


if __name__ == '__main__':
    app.run(host='localhost', debug=True, port=8080)
