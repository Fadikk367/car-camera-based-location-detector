from flask import request
from werkzeug.utils import secure_filename
import os
import cv2
from .extractors.plates.plate_analyzer import predict_country_from_plate
from .extractors.plates.plate_detector import getPlates

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'yaml'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_file_from_request():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        path = os.path.join('images', filename)
        file.save(path)
        return cv2.imread(path)
    else:
        raise WrongFileExtension()

def extract_data_from_plates(image):
    countries = []
    for plate in getPlates(image):
        countries += predict_country_from_plate(plate)
    return countries

class WrongFileExtension(Exception):
    pass

upload_form = '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''