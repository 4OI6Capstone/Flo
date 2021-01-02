from flask import Flask
from flask import request
from utils.songs.SongClassifier import SongClassifier
import uuid

app = Flask(__name__)


@app.route("/get-mix", methods=['POST'])
def getmix():
    song_list = request.files.getlist("files")
    song_classifier = SongClassifier()
    request_id = uuid.uuid4()
    song_classifier.deconstruct_songs(song_list, request_id)


if __name__ == '__main__':
    app.run(host='localhost', debug=True, port=8080)
