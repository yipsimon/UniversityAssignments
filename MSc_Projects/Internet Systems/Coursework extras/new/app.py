from flask import Flask, jsonify, abort, request
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient()
db = client.test_database

stations = db.stations
mobiles = db.mobiles

stations = [
			    {
			        'id': 1,
			        'location': u'Loughborough',
			        'capacity': 50,
			        'timestamp': 978307200
			    },
			    {
			        'id': 2,
			        'location': u'Leicester',
			        'capacity': 50, 
			        'timestamp': 1136073600
			    },
			    {
			        'id': 3,
			        'location': u'Derby',
			        'capacity': 50, 
			        'timestamp': 1167609600
			    },
			    {
			        'id': 4,
			        'location': u'Nottingham',
			        'capacity': 50, 
			        'timestamp': 1325376000
			    },
			    {
			        'id': 5,
			        'location': u'Birmingham',
			        'capacity': 50, 
			        'timestamp': 1483228800
			    },
			]

@app.route('/', methods=['GET'])
def create():
	return "This is fine"

@app.route('/basestation', methods=['GET'])
def get_all_stations():
	return jsonify({'Base Stations': stations})

# example: www.sci-project.lboro.ac.uk/basestation/1
@app.route('/basestation/<int:id>', methods=['GET'])
def get_station(id):
    station = [station for station in stations if station['id'] == id]
    if len(station) == 0:
        abort(404)
    return jsonify({'Station': station})

# example: www.sci-project.lboro.ac.uk/basestation/1/07508281950
@app.route('/basestation/<int:id>/<int:number>', methods=['POST'])
def mobile_connect(id, number):
	pass

if __name__ == '__main__':
	app.run(debug=True)