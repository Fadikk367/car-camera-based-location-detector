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
    number_of_frames = len(frames)

    for index, frame in enumerate(frames):
        print(f'Start extracting data from plates for frame {index + 1} of {number_of_frames}')
        for country in extract_data_from_plates(frame):
            data['countries'][country] += weights['plate']

        print(f'Start extracting data from route for frame {index + 1} of {number_of_frames}')
        countries, probability = extract_data_from_route(frame)
        for country in countries:
            data['countries'][country] += weights['route'] * probability

        print(f'Start extracting data from text for frame {index + 1} of {number_of_frames}')
        countries_from_text, words = extract_data_from_text(frame)
        for country in countries_from_text.items():
            data['countries'][country[0]] += weights['plate'] * country[1]

        for word in words:
            print(f'Chcecking word: {word}')
            data['markers'].append(get_cities_from_string(word))

        data['markers'].append(get_cities_from_string('bialystok'))

    return {'result': data}, 200
