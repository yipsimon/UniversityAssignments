from flask import Flask, jsonify, abort, request
from pymongo import MongoClient
import json

app = Flask(__name__)

client = MongoClient("mongodb://cosyly:4JbHBLrBqK@sci-project:27017/cosyly")
db = client.cosyly

@app.route('/basestation', methods=['POST'])
def insert_stations():
	data1 = json.loads(request.data)
	#data1 = request.json[]
	db.BaseStation.insert_one({"stationid":data1['id'],"stationname":data1['name'],"location":data1['location'],"capacity":data1['capacity'],'timestarted':data1['time'],'street':data1['street'],'county':data1['county']})
	print 'id: '+str(data1['id'])+'\nBasestation: '+data1['name']+'\nLocation: '+data1['location']+'\nCapacity: '+str(data1['capacity'])+'\nSuccessfully Started\n'
	return json.dumps({'success':True}), 201
#, {'ContentType':'application/json'}

# example: www.sci-project.lboro.ac.uk/basestation/1/07508281950
@app.route('/mobiledata', methods=['POST'])
def mobile_connect():
	data2 = json.loads(request.data)
	db.MobileData.insert_one({
		"stationid":data2['stationid'],
		"number":data2['number'],
		"message":data2['message'],
		"timeofconnection":data2['timeofconnection']
		})
	print str(data2['number'])+" connected to "+str(data2['stationid'])+"\n"
	return json.dumps({'success':True}), 201

@app.route('/mobiledata/<string:id>/<int:number>', methods=['DELETE'])
def mobile_disconnect(id, number):
	#check for existing id in database first
	db.MobileData.delete_one({"number": number,"stationid": id})
	print "Disconnected from "+str(number)
	return 'Received',200

#Reponse for every situation

if __name__ == '__main__':
	app.run(debug=True)



# example: www.sci-project.lboro.ac.uk/basestation/1
@app.route('/basestation/<string:loc>', methods=['GET'])
def get_station(loc):
	data = db.BaseStation.find({'location':loc})

@app.route('/', methods=['GET'])
def create():
	return "This is fine"

#col = db.BaseStation.insert()
