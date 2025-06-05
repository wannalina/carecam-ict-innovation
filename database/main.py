from flask import Flask, jsonify
#from flask_cors import CORS

app = Flask(__name__)
#CORS(app, origins=['insert_url_here']) # required for when deployed

@app.route('/', methods=['GET'])
def basic_route():
    return jsonify({'message': 'Base route works!'})

if __name__ == "__main__":
    app.run(debug=True)