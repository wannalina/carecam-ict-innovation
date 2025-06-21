from flask import Flask, jsonify, request
import os
import json
#from flask_cors import CORS

app = Flask(__name__)
#CORS(app, origins=['insert_url_here']) # required for when deployed

PATIENT_DATA_FILE = 'patient_data.json'

# route to test basic app functionality
@app.route('/', methods=['GET'])
def basic_route():
    return jsonify({'message': 'Base route works!'})

# route to post image for facial recognition; returns patient medical data
@app.route('/get-patient-data-from-image', methods=['POST'])
def facial_recognition_route():
    try:
        request_body = request.get_json()
        image = request_body.get('image')

        if image: 
            # load data from json file
            with open(PATIENT_DATA_FILE, 'r') as f:
                patient_data = json.load(f)

            # insert image into entry image field
            patient_data[0]['image'] = image

            # return patient data to raspberrypi
            return jsonify({'message': patient_data['patients'][0]}), 200
    except Exception as e:
        return jsonify({f'message': 'Error in facial recognition: {e}'}), 500

if __name__ == "__main__":
    app.run(debug=True)