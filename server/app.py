from flask import Flask, request
from flask_cors import CORS

from .services import *


app = Flask(__name__)
CORS(app)

if __name__ == '__main__':
    app.run()

weights = {
    'plate': 0.2
}

@app.route('/', methods=['GET', 'POST'])
def predict():
    if request.method == 'GET':
        return upload_form

    data = {
        'countries': {},
        'markers': []
    }

    try:
        video_path = get_file_from_request()
    except WrongFileExtension:
        return {'message': 'Wrong file extension'}, 400

    frames = get_frames_from_video(video_path)

    # for country in extract_data_from_plates(image):
        # data['countries'][country] = weights['plate']


    # kierunek jazdy -> lista krajów
    # text extraktor -> lista krajów z prawdopodobieństwami i lista stringów
    # zapytanie do api czy któryś z tych stringów jest miastem, jak tak to pakumey do markerów
    # zwracamy

    return {'result': data}, 200
