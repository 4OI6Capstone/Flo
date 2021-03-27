from flask import Flask, send_file
from flask_cors import CORS, cross_origin
from flask import request
from utils.augmentation.Augmentor import Augmentor
from utils.songs.SongClassifier import SongClassifier
import uuid
import pathlib
import logging

app = Flask(__name__)
CORS(app, support_credentials=True)
app.config['EXPORT_FOLDER'] = "./mixes/"
app.config['UPLOADED_FOLDER'] = "./uploaded_files/"
logging.basicConfig(filename='app.log', level=logging.INFO,
                    format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
logging.getLogger().addHandler(logging.StreamHandler())
logging.getLogger("musicbrainzngs").setLevel(logging.WARNING)


@app.route("/get-mix", methods=['POST'])
def getmix():
    # Takes request's files
    song_list = request.files.getlist("files")
    # Initialize song classifier object
    song_classifier = SongClassifier()
    # Create random request Id
    request_id = uuid.uuid4()
    app.logger.info("Received request with request Id: {}".format(str(request_id)))
    # Creates request working directory
    create_request_dir(str(request_id))
    # Get Music Brainz and Acoustic Brainz info
    app.logger.info("Beginning song classification for request Id: {}".format(str(request_id)))
    song_classifier.deconstruct_songs(song_list, request_id)
    # Creates Augmentor for the mix
    app.logger.info("Beginning song augmentation for request Id: {}".format(str(request_id)))
    augmentor = Augmentor(song_classifier.song_list.get(str(request_id)))
    # Creates the mix
    app.logger.info("Creating final mix for request Id: {}".format(str(request_id)))
    final_mix = augmentor.create_mix(request_id)
    # Export
    file_path = app.config['EXPORT_FOLDER'] + str(request_id) + "/final_mix.mp4"
    app.logger.info("Exporting final mix for request Id: {} to {}".format(str(request_id), file_path))
    final_mix.export(file_path, format="mp4")
    # Returns request Id for particular mix
    try:
        return send_file('./mixes/8e1a1fbd-c001-454f-9057-e822a617898a/final_mix.mp4', attachment_filename="final_mix.mp4")
    except Exception as e:
        return str(e)


def create_request_dir(request_id):
    request_export_dir = app.config['EXPORT_FOLDER'] + request_id
    request_upload_dir = app.config['UPLOADED_FOLDER'] + request_id
    pathlib.Path(request_export_dir).mkdir(parents=True, exist_ok=True)
    pathlib.Path(request_upload_dir).mkdir(parents=True, exist_ok=True)


if __name__ == '__main__':
    pathlib.Path(app.config['EXPORT_FOLDER']).mkdir(parents=True, exist_ok=True)
    pathlib.Path(app.config['UPLOADED_FOLDER']).mkdir(parents=True, exist_ok=True)
    app.run(host='localhost', debug=True, port=8080)