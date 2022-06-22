from flask import Flask, request
from flask_cors import CORS

from .services import *
from .extractors.plates.plate_analyzer import predict_country_from_plate
from .extractors.plates.plate_detector import getPlates

app = Flask(__name__)
CORS(app)

if __name__ == '__main__':
    app.run()

@app.route('/', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        # Get file
        try:
            image = get_file_from_request()
        except WrongFileExtension:
            return {'message': 'Wrong file extension'}, 400
        for plate in getPlates(image):
            print(predict_country_from_plate(plate))
        # plate -> lista krajów
        # kierunek jazdy -> lista krajów
        # text extraktor -> lista krajów z prawdopodobieństwami i lista stringów
        # zapytanie do api czy któryś z tych stringów jest miastem, jak tak to pakumey do markerów
        # zwracamy

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