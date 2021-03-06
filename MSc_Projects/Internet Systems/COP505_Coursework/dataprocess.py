from flask import Flask, jsonify, abort, request
from pymongo import MongoClient
from bson.json_util import dumps
from itertools import chain
import json

app = Flask(__name__)

client = MongoClient("mongodb://cosyly:4JbHBLrBqK@sci-project:27017/cosyly")
db = client.cosyly

@app.route('/basestation', methods=['GET', 'POST'])
def insert_stations():
	if request.method == 'POST':
		data1 = json.loads(request.data)
		db.BaseStation.insert_one({"stationid":data1['id'],
				"stationname":data1['name'],
				"location":data1['location'],
				"capacity":data1['capacity'],
				'timestarted':data1['time'],
				'street':data1['street'],
				'county':data1['county']
		})
		print 'id: '+str(data1['id'])+'\nBasestation: '+data1['name']+'\nLocation: '+data1['location']+'\nCapacity: '+str(data1['capacity'])+'\nSuccessfully Started\n'
		return json.dumps({'success':True}), 201
	else:
		cursor = db.BaseStation.find({},{'_id':0})
		return dumps(cursor)

@app.route('/basestation/getid/<string:id>', methods=['GET'])
def get_station_data(id):
	cursor = db.MobileData.find({"stationid":id},{'_id':0})
	return dumps(cursor)

@app.route('/basestation/getloc/<string:city>', methods=['GET'])
def get_station_data_city(city):
	cursor = db.BaseStation.find({"location":city},{'_id':0})
	return dumps(cursor)

@app.route('/basestation/<string:id>', methods=['DELETE'])
def stop_stations(id):
	db.BaseStation.delete_one({"stationid":id})
	print "Base station: "+str(id)+" terminated"
	return 'Received',200

@app.route('/basestation/busy', methods=['GET'])
def busy_stations():
	output = []
	cursor1 = db.BaseStation.find({},{'_id':0})
	for record in cursor1:
		cursor2 = db.MobileData.find({'stationid':record['stationid']},{'_id':0})
		num = cursor2.count()
		pencent = ( num / float(record['capacity']) )*100
		if pencent >= 90:
			temp = db.BaseStation.find({'stationid':record['stationid']},{'_id':0})
			output = [x for x in chain(output,temp)]

	return dumps(output)

@app.route('/basestation/stat', methods=['GET'])
def stat_stations():
	output = []
	cursor1 = db.BaseStation.find({},{'_id':0})
	for record in cursor1:
		cursor2 = db.MobileData.find({'stationid':record['stationid']},{'_id':0})
		num = cursor2.count()
		cap = record['capacity']
		pencent = ( num / float(record['capacity']) )*100
		data = {'stationid':record['stationid'], 'stationname':record['stationname'], 'capacity':record['capacity'], 'connected':num, 'percent':pencent}
		output.append(data)

	return dumps(output)

@app.route('/mobiledata', methods=['POST'])
def mobile_connect():
	data2 = json.loads(request.data)
	db.MobileData.insert_one({
		"stationid":data2['stationid'],
		"number":data2['number'],
		"message":data2['message'],
		"timeofconnection":data2['timeofconnection']
		})
	print str(data2['number'])+" connected to "+str(data2['stationid'])+""
	return json.dumps({'success':True}), 201

@app.route('/mobiledata/<string:id>/<int:number>', methods=['DELETE'])
def mobile_disconnect(id, number):
	#check for existing id in database first
	db.MobileData.delete_one({"number": '0'+str(number),"stationid":str(id)})
	print "Disconnected from "+'0'+str(number)
	return 'Received',200

if __name__ == '__main__':
	app.run(debug=True)

@app.route('/', methods=['GET'])
def create():
	print "This is fine"
	return "This is fine"

#cursor1 = db.BaseStation.find({}{'_id':0, 'stationid':1, 'stationname':1, 'capacity':1})
