from flask import Flask
from flask import request
from utils.augmentation.Augmentor import Augmentor
from utils.songs.SongClassifier import SongClassifier
import uuid
import pathlib

app = Flask(__name__)
app.config['EXPORT_FOLDER'] = "./mixes/"
app.config['UPLOADED_FOLDER'] = "./uploaded_files/"


@app.route("/get-mix", methods=['POST'])
def getmix():
    song_list = request.files.getlist("files")
    song_classifier = SongClassifier()
    request_id = uuid.uuid4()
    create_request_dir(str(request_id))
    song_classifier.deconstruct_songs(song_list, request_id)
    augmentor = Augmentor(song_classifier.song_list.get(str(request_id)))
    final_mix = augmentor.create_mix()
    final_mix.export(app.config['EXPORT_FOLDER'] + str(request_id) + "/final_mix.mp4", format="mp4")
    print("done")
    return "done"


def create_request_dir(request_id):
    request_export_dir = app.config['EXPORT_FOLDER'] + request_id
    request_upload_dir = app.config['UPLOADED_FOLDER'] + request_id
    pathlib.Path(request_export_dir).mkdir(parents=True, exist_ok=True)
    pathlib.Path(request_upload_dir).mkdir(parents=True, exist_ok=True)


if __name__ == '__main__':
    app.run(host='localhost', debug=True, port=8080)
    pathlib.Path(app.config['EXPORT_FOLDER']).mkdir(parents=True, exist_ok=True)
    pathlib.Path(app.config['UPLOADED_FOLDER']).mkdir(parents=True, exist_ok=True)
