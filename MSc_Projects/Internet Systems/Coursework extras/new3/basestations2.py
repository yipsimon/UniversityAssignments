from threading import Thread
import time, random, traceback, uuid
import requests
import json
import Queue
from socket import socket, AF_INET, SOCK_STREAM

exitFlag = 0

class basestation():
    def __init__(self, name, city, street, county, capacity):
        self.id = str(uuid.uuid4().get_hex().lower()[0:8])
        self.name = name
        self.location = city
        self.capacity = capacity
        self.street = street
        self.county = county

def postdata(data,dir):
    #url = "http://127.0.0.1:5000/basestation"
    #url = "http://cosyly@sci-project:5001/basestation" working
    url = "http://cosyly@sci-project:5001/"+str(dir)
    #url = "http://cosyly@sci-project.lboro.ac.uk:8080/todo/ap7/v1.0/tasks/"+dir
    #basestation"
    payload = json.dumps(data)
    r = requests.post(url, payload)
    #print str(r.status_code)
    '''
    count = 0
    while r.status_code > 202:
        if count < 5:
            print r.status_code,"Retry in 5 seconds"
            time.sleep(5)
            r = requests.post(url, payload)
            print r.status_code
            count += 1
        else:
            print "Fail to send data"
            break
    '''

def deletdata(dir):
    #url = "http://127.0.0.1:5000/"+dir
    url = "http://cosyly@sci-project:5001/"+str(dir)
    r = requests.delete(url)
    #print str(r.status_code)
    '''
    count = 0
    while r.status_code > 202:
        if count < 5:
            print r.status_code,"Retry in 5 seconds"
            time.sleep(5)
            r = requests.delete(url)
            count += 1
        else:
            print "Fail to send data"
            break
    '''
#def updatedata(dir):

class mobile():
    def __init__(self):
        self.number = '07' + ''.join(["%s" % random.randint(0, 9) for num in range(0, 9)])
        self.conlimit = random.randint(0, 2)
        self.loc = station.location

    def connect(self,mess):
        #print "Mobile: "+str(self.number)+", Starting connection to "+self.loc+", conlimit:"+str(self.conlimit)
        data = {'number':self.number,'message':mess,'timeofconnection':time.time(),'stationid':station.id}
        #data_string = json.dumps(data) #data serialized
        postdata(data,'mobiledata')

    def disconnect(self):
        delurl = "mobiledata/"+str(station.id)+"/"+str(self.number)
        deletdata(delurl)

    def __cmp__(self, other):
                return cmp(self.conlimit, other.conlimit)

def connection(threadname, q, count):
    while count:
        newconnect = mobile()
        newconnect.connect('Hello')
        q.put(newconnect)
        count -= 1
        time.sleep(random.randint(0,3))
        if exitFlag:
            break


def disconnection(threadname, q):
    time.sleep(6)
    while not q.empty():
        next_job = q.get()
        time.sleep(next_job.conlimit)
        next_job.disconnect()
        #print 'Ending job: ', next_job.number
        #count+=1

'''
class myThread(Thread):
    def __init__(self, name, mode, q):
        Thread.__init__(self)
        self.name = name
        self.mode = mode
        self.queue = q
        self.count = 4
    def run(self):
        print "Starting "+self.name
        if self.mode == 'c':
            while self.count:
                newconnect = mobile()
                newconnect.connect('Hello')
                self.queue.put(newconnect)
                self.count -= 1
                time.sleep(random.randint(0,3))
                if exitFlag:
                        Thread.exit()
            Thread.exit()
        if self.mode == 'd':
            time.sleep(6)
            while not self.queue.empty():
                next_job = self.queue.get()
                time.sleep(next_job.conlimit)
                next_job.disconnect()
                #print 'Ending job: ', next_job.number
                #count+=1
            Thread.exit()

        print "Exiting "+self.name
'''

f = open('ports.txt','r')
output = []
for x in f.readlines():
    output.append(x[0])
f.close()

if len(output) == 0:
    print "List of Activated Base Station: None"
else:
    print "List of Activated Base Stations: "
    for item in output:
        print item+', '


stationName = raw_input("\nName of the station: ")
stationLocation = raw_input("City of the station: ")
streetname = raw_input("Street name of the station: ")
statcounty = raw_input("County of the station: ")
stationCapacity = int(input("Capacity of the station: "))

station = basestation(stationName, stationLocation,streetname,statcounty, stationCapacity)
data = {'id':station.id, 'name':station.name, 'street':streetname,'county':statcounty, 'location':station.location, 'capacity':station.capacity, 'time':time.time()}
postdata(data,"basestation")
print "Connected, Base station: "+stationName+" activated\n"

output.append(stationName)

x = raw_input('Press Enter to generate mock mobile connections: ')

queueing = Queue.PriorityQueue()
#exitFlag = False
'''
thread1 = myThread('T1','c',queueing)
thread2 = myThread('T2','d',queueing)

thread1.start()
thread2.start()

x = raw_input('\nEnter Stop to End')
if x == 'stop':
    exitFlag = 1

thread1.join()
thread2.join()
'''

connection("Process1",queueing,5)
disconnection("Process2",queueing)

'''
thread.start_new_thread( connection, ("cthread1", queueing, ))
thread.start_new_thread( disconnection, ("dthread1", queueing, ))
time.sleep(4)
'''

print 'finish'
#exitFlag = True

'''

f = open('ports.txt','r')
exitput = []
for x in f.readlines():
    if stationName not in x.split():
        exitput.append(x)
f.close()
f = open('ports.txt','w')
for item in exitput:
    f.write(item)
f.close()
'''


'''
s = socket(AF_INET, SOCK_STREAM)
#port = dicbasestation[stationName]
s.bind( ("127.0.0.1", 5000) )
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
s.listen(50)


dellist = []
postlist = []
cap = stationCapacity

while True:
    conn,addr=s.accept()
    print "Connection received from ",conn,addr
    data = conn.recv(1024)
    data_loaded = json.loads(data)
    print data_loaded['message']
    if data_loaded == "Bye":
        data2 = "Number: "+data_loaded['number']+" Disconnected from "+stationName
        conn.send(data2)
        delurl = "mobiledata/"+str(station.id)+"/"+str(data_loaded['number'])
        #mobiledata = {'number':data['number'],'stationid':station.id}
        deletdata(delurl)
        conn.close()
        cap += 1
    else:
        data2 = "Number: "+data_loaded['number']+" Connected to "+stationName
        conn.send(data2)
        mobiledata = {'number':data_loaded['number'],'message':data_loaded['message'],'timeofconnection':time.time(),'stationid':station.id}
        postdata(mobiledata,'/mobiledata')
        conn.close()
        cap -= 1

		data2 = "Number: "+data_loaded['number']+" Connected to "+stationName
		conn.send(data2)
		mobiledata = {'number':data_loaded['number'],'message':data_loaded['message'],'timeofconnection':time.time(),'stationid':station.id}
		postdata(mobiledata,'/mobiledata')
		conn.close()
		cap -= 1

'''
