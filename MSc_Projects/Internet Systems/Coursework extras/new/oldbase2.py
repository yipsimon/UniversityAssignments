from threading import Thread
import time, random, traceback, uuid
from socket import socket, AF_INET, SOCK_STREAM
import requests
import json

class basestation():
    def __init__(self, stationname, location, capacity):
        self.id = str(uuid.uuid4().get_hex().lower()[0:8])
        self.name = stationname
        self.location = location
        self.capacity = capacity

def postdata(self,url,data):
    #data=json.dumps(data)
    r = requests.post(url,json = data)
    if r.status_code == 200: #requests.codes.ok
        print "Data is sent"

url = "http://cosyly@sci-project.lboro.ac.uk"
stationName = raw_input("\n Insert the name of the base station: ")
stationLocation = raw_input("Location of the station: ")
stationCapacity = int(input("Select the station's capacity: "))

station = basestation(stationName, stationLocation, stationCapacity)
data = {'Uniqueid':station.id,'Location':station.location,'Capacity':station.capacity,'Time':time.time()}
#postdata(url,data)

s = socket(AF_INET, SOCK_STREAM)
#port = dicbasestation[stationName]
s.bind( ("127.0.0.1", 0) )
print "Connected, Base station: "+stationName+" activated, Port number: "+str(s.getsockname()[1])+"\n"
f = open('ports.txt','r')
output = []
for x in f.readlines():
    if stationName not in x.split():
        output.append(x)
f.close()
output.append(stationName+" "+str(s.getsockname()[1])+"\n")
print output
f = open('ports.txt','w')
for item in output:
    f.write(item)
f.close()
s.listen(5)

receivedlist = []

while True:
    conn,addr=s.accept()
    print "Connection received from ",conn,addr
    data = conn.recv(1024)
    data_loaded = json.loads(data)
    print data_loaded['Message']
    if data_loaded == "Bye":
        data2 = "Number: "+data_loaded['Number']+" Disconnected from "+stationName
        conn.send(data2)
	#mobiledata = {'Number':data['Number'],'BaseStation':stationName}
	#deletedata(url,mobiledata)
	#senddata = {'Phone_number':int(data),'Start_connection': int(time.time()), 'Location':str(stationName)}
        conn.close()
    else:
        data2 = "Number: "+data_loaded['Number']+" Connected to "+stationName
        conn.send(data2)
	#mobiledata = {'Number':data['Number'],'Message':data['Message'],'Timeofconnection':time.time(),'BaseStation':stationName}
	#postdata(url,mobiledata)
	#senddata = {'Phone_number':int(data),'Start_connection': int(time.time()), 'Location':str(stationName)}
        conn.close()






'''
if data!="Exit":
            print "received ", data
            data2 = " Connected to "+stationName
            conn.send(data2)
            #senddata = {'Phone_number':int(data),'Start_connection': int(time.time()), 'Location':str(stationName)}

        else:
            #close the connection
            print "received ", data
            data2 = " Closed connection to "+stationName
            conn.send(data2)
            conn.close()
            break
'''
