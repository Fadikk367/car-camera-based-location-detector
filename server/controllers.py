
from flask import Blueprint, request

from services import *

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/image', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Get file
        try:
            get_file_from_request()
        except WrongFileExtension:
            return {'message': 'Wrong file extension'}, 400
        # use extractor

        return {'message': 'Success'}, 200
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''