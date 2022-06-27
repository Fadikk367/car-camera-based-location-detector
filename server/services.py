from flask import request
from werkzeug.utils import secure_filename
import os
import cv2
import requests
from .extractors.text_extractor.text_extractor import extract_all
from .extractors.plates.plate_analyzer import predict_country_from_plate
from .extractors.plates.plate_detector import getPlates
from .extractors.traffic_side_extractor.traffic_side_extractor import traffic_side_extractor

ALLOWED_EXTENSIONS = {'mp4'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_file_from_request():
    if 'file' not in request.files:
        raise FileInputTypeNonExistent()
    file = request.files['file']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        raise EmptyFile()
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        video_path = os.path.join('images', filename)
        file.save(video_path)
        return video_path
    else:
        raise WrongFileExtension()

def get_frames_from_video(video_path):
    reader = cv2.VideoCapture(video_path)
    is_next_frame, frame = reader.read()
    all_frames = []
    i = 0
    while is_next_frame:
        i += 1
        all_frames.append(frame)
        is_next_frame, frame = reader.read()
    reader.release()
    div = i//int(request.form['frames']) + 1
    frames = [frame for index, frame in enumerate(all_frames) if index%div == 0]
    print(f'Result number of frames: {len(frames)}')
    return frames

def extract_data_from_plates(image):
    countries = []
    for plate in getPlates(image):
        countries += predict_country_from_plate(plate)
    return countries

def extract_data_from_text(image):
    countries = {}
    words = []
    for model_result in extract_all(image):
        languages = model_result[0]
        for language in languages:
            countries[language.lang] = language.prob
        model_words = model_result[1]
        for word in model_words:
            if len(word) > 3:
                words.append(word)
    return countries, words

def extract_data_from_route(image):
    return traffic_side_extractor(image)

def get_cities_from_string(string):
    response = requests.get(f'https://graphhopper.com/api/1/geocode?q={string}&debug=true&key=9b5dc8fa-e030-418a-8011-17472be5b1bb').json()
    hits = response['hits']
    if len(hits) > 0:
        return {'point': hits[0]['point'], 'name': hits[0]['name']}

class WrongFileExtension(Exception):
    pass

class EmptyFile(Exception):
    pass

class FileInputTypeNonExistent(Exception):
    pass

upload_form = '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
      <input type=number name=frames>
    </form>
    '''