from flask import Flask, jsonify, abort, request
from pymongo import MongoClient
import json

app = Flask(__name__)

stations = []

client = MongoClient("mongodb://cosyly:4JbHBLrBqK@sci-project:27017/cosyly")
db = client.cosyly

@app.route('/', methods=['GET'])
def create():
	return "This is fine"

#col = db.BaseStation.insert()

@app.route('/basestation', methods=['POST'])
<<<<<<< HEAD
def insert_stations():
	data1 = json.loads(request.data)
	#data1 = request.json[]
   	db.BaseStation.insert_one({"stationid":data1['id'],"location":data1['location'],"capacity":data1['capacity'],'timestarted':data1['time'],'street':data1['street'],'county':data1['county']})
=======
def create_station():
	data = json.loads(request.data)
   	db.BaseStation.insert_one({"stationid":data['id'],"location":data['location'],"capacity":data['capacity'],'timestarted':data['time'],'street':data['street'],'county':data['county']})
>>>>>>> 75a38499de6ca48c55bcb014ebd62919a44060e3
	print '\nInserted data successfully\n'
	return json.dumps({'success':True}), 201, {'ContentType':'application/json'} 
	
@app.route('/basestation', methods=['GET'])
def get_all_stations():
	return jsonify({'Base Stations': stations})

<<<<<<< HEAD
# example: www.sci-project.lboro.ac.uk/basestation/1
@app.route('/basestation/<string:loc>', methods=['GET'])
def get_station(loc):
	data = db.BaseStation.find({'location':loc})
	'''
=======
@app.route('/basestation/<string:id>', methods=['GET'])
def get_station(id):
>>>>>>> 75a38499de6ca48c55bcb014ebd62919a44060e3
    station = [station for station in stations if station['id'] == id]
    if len(station) == 0:
        abort(404)
	'''
    return jsonify({'Station': station})

# example: www.sci-project.lboro.ac.uk/basestation/1/07508281950
@app.route('/mobiledata', methods=['POST'])
def mobile_connect():
	mdata = request.data
	db.MobileData.insert_one({'number':mdata['number'],'message':mdata['message'],'timeofconnection':mdata['timeofconnection'],'stationid':mdata['id']})
	print str(mdata['number'])+" connected"
	return 'Received',200
	
@app.route('/mobiledata/<string:id>/<int:number>', methods=['DELETE'])
def mobile_disconnect(id, number):
	#check for existing id in database first
	db.MobileData.delete_one({'number': number,'stationid': id})
	print "Disconnected from "+str(number)
	return 'Received',200
	
#Reponse for every situation
if __name__ == '__main__':
	app.run(debug=True)