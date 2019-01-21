from flask import Flask, jsonify, abort, request
from pymongo import MongoClient
import json

app = Flask(__name__)

@app.route('/', methods=['GET'])
def create():
	return "Go to /basestation to see the list of base stations."

@app.route('/basestation', methods=['GET'])
def get_all_stations():
	return jsonify({'Base Stations': stations})

@app.route('/basestation', methods=['POST'])
def create_station():
	data = json.loads(request.data)
	print data

	return "hi"

# example: www.sci-project.lboro.ac.uk/basestation/1
@app.route('/basestation/<string:id>', methods=['GET'])
def get_station(id):
    station = [station for station in stations if station['id'] == id]
    if len(station) == 0:
        abort(404)
    return jsonify({'Station': station})

# example: www.sci-project.lboro.ac.uk/basestation/eg7sect5/07508281950
@app.route('/basestation/<string:id>/<int:number>', methods=['POST'])
def mobile_connect(id, number):
	print number + " is connecting to base station ID " + id 

@app.route('/basestation/<string:id>/<int:number>', methods=['DELETE'])
def mobile_disconnect(id, number):
	pass

if __name__ == '__main__':
	app.run(debug=True)