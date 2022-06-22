from flask import Flask, request
from flask_cors import CORS
from .extractors.text_extractor.text_extractor import extract_all
from .services import *


app = Flask(__name__)
CORS(app)

if __name__ == '__main__':
    app.run()

weights = {
    'plate': 0.2,
    'lang': 0.7,
    'route': 0.1
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

    print(f'start extracting data from plates')
    # for country in extract_data_from_plates(frames[0]):
        # data['countries'][country] = weights['plate']

    print(f'start extracting data from text')
    countries_from_text, words = extract_data_from_text(frames[0])
    for country in countries_from_text.items():
        data['countries'][country[0]] = weights['plate'] * country[1]

    for word in words:
        print(f'word: ======== {word}')
        # data['markers'].append(get_cities_from_string(word))

    # zwracamy

    return {'result': data}, 200
