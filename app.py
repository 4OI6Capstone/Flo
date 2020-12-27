from flask import Flask
from flask import request
from utils.songs import SongClassifier


app = Flask(__name__)


@app.route("/get-mix", methods=['POST'])
def getmix():
    song_list = request.files.getlist("files")
    song_classifier = SongClassifier()
    song_classifier.deconstruct_songs(song_list)


if __name__ == '__main__':
    app.run(host='localhost', debug=True, port=8080)
