import threading
import time, random, traceback, uuid
import requests
import json
import Queue
from socket import socket, AF_INET, SOCK_STREAM

threadLock = threading.Lock()
global_count = 0
'''
with threadLock:
    global_count += 1
'''

def add_count():
    global global_count
    with threadLock:
        global_count += 1

def subt_count():
    global global_count
    with threadLock:
        global_count -= 1

def check_count():
    global global_count
    with threadLock:
        if global_count == 0:
            return False
        else:
            return True

def get_count():
    global global_count
    with threadLock:
        return global_count

class mobile():
    def __init__(self):
        self.number = '07' + ''.join(["%s" % random.randint(0, 9) for num in range(0, 9)])
        self.conlimit = random.randint(0, 5)
        self.loc = station.location

    def connect(self,mess,q):
        #print "Mobile: "+str(self.number)+", Starting connection to "+self.loc+", conlimit:"+str(self.conlimit)
        self.data = {'number':self.number,'message':mess,'timeofconnection':time.time(),'stationid':station.id}
        #data_string = json.dumps(data) #data serialized
        postdata(self.data,'mobiledata',q)

    def disconnect(self,q):
        delurl = "mobiledata/"+str(station.id)+"/"+str(self.number)
        deletdata(delurl,q)

    def __cmp__(self, other):
                return cmp(self.conlimit, other.conlimit)

class basestation():
    def __init__(self, name, city, street, county, capacity):
        self.id = str(uuid.uuid4().get_hex().lower()[0:8])
        self.name = name
        self.location = city
        self.capacity = capacity
        self.street = street
        self.county = county

class failreq(object):
    def __init__(self, type, data1, dir):
        self.type = type
        self.data = data1
        self.dir = dir

def postdata(data,dir,q):
    #url = "http://127.0.0.1:5001/basestation"
    #url = "http://cosyly@sci-project:5001/basestation" working
    #url = "http://cosyly@sci-project.lboro.ac.uk:8080/todo/ap7/v1.0/tasks/"+dir
    #url = "http://cosyly@sci-project:5001/"+str(dir)
    url = "http://127.0.0.1:5001/"+str(dir)
    payload = json.dumps(data)
    try:
        r = requests.post(url, payload)
        r.raise_for_status()
        subt_count()
    except requests.exceptions.ConnectionError as e:
        print e
        print "connection error, fall to send data"
        q.put(failreq('post',data,dir))
        time.sleep(5)
    except requests.exceptions.HTTPError as err:
        print err
        print "http requests error",r.status_code
        print "fail to send data"
    except requests.exceptions.RequestException as error:
        print error
        print "Fatal Error Terminating"
        sys.exit(1)


def deletdata(dir,q):
    #url = "http://127.0.0.1:5001/basestation"
    #url = "http://cosyly@sci-project:5001/basestation" working
    #url = "http://cosyly@sci-project.lboro.ac.uk:8080/todo/ap7/v1.0/tasks/"+dir
    #url = "http://cosyly@sci-project:5001/"+str(dir)
    url = "http://127.0.0.1:5001/"+str(dir)
    try:
        r = requests.delete(url)
        r.raise_for_status()
        add_count()
    except requests.exceptions.ConnectionError as e:
        print e
        print "connection error, fall to send data"
        q.put(failreq('del',dir,dir))
        time.sleep(5)
        add_count()
    except requests.exceptions.HTTPError as err:
        print err
        print "http requests error",r.status_code
        print "fail to send data"
    except requests.exceptions.RequestException as error:
        print error
        print "Fatal Error Terminating"
        sys.exit(1)


#def updatedata(dir):
'''
def connection(q,errq):
    while True:
        newconnect = mobile()
        newconnect.connect('Hello',errq)
        q.put(newconnect)
        time.sleep(random.randint(0,3))
def disconnection(q, errq):
    time.sleep(6)
    while not q.empty():
        next_job = q.get()
        time.sleep(next_job.conlimit)
        next_job.disconnect(errq)
def offline(errq,running):
    while True:
        while not errq.empty():
            job = errq.get()
            if job.type == 'post':
                postdata(job.data,job.dir,errq)
            if job.type == 'del':
                deletdata(job.dir,errq)
'''

class myThread(threading.Thread):
    def __init__(self,mode,q,errq):
        threading.Thread.__init__(self)
        self.mode = mode
        self.q = q
        self.errq = errq
        self.run1 = True
        self.gconnect = True
        self.count = True
        self.quit = False

    def run(self):
        if self.mode == 'connect':
            while self.run1:
                self.count = check_count()
                if self.gconnect and self.count:
                    if self.errq.empty():
                        newconnect = mobile()
                        newconnect.connect('Hello',self.errq)
                        self.q.put(newconnect)
                        time.sleep(random.randint(0,3))
                else:
                    print 'maxed count'
                    time.sleep(2)



        if self.mode == 'disconnect':
            time.sleep(6)
            while self.run1:
                while not self.q.empty():
                    next_job = self.q.get()
                    wait = next_job.conlimit
                    if self.quit:
                        wait = 0
                    time.sleep(wait)
                    #time.sleep(1)
                    next_job.disconnect(self.errq)


        if self.mode == 'memoryreqs':
            while self.run1:
                while not self.errq.empty():
                    #self.count = check_count
                    job = self.errq.get()
                    if job.type == 'post':
                        #if self.count:
                            postdata(job.data,job.dir,self.errq)
                            time.sleep(random.randint(0,5))
                            delurl2 = "mobiledata/"+str(job.data['stationid'])+"/"+str(job.data['number'])
                            deletdata(delurl2,self.errq)
                    if job.type == 'del':
                        deletdata(job.dir,self.errq)

    def startpause(self):
        if self.gconnect:
            self.gconnect = False
            print 'Generate connection is false'
        else:
            self.gconnect = True
            print 'Generate connection is true'

    def termination(self):
        self.gconnect = False
        print 'Generate connection is false'
        self.quit = True
        while not self.errq.empty():
            pass
        print 'errq empty'
        while not self.q.empty():
            pass
        print 'q empty'
        self.run1 = False
'''
def count(mode):
    global capcount
    print 'started'
    if mode == 'post':
        cap_lock.acquire()
        capcount -= 1
        if capcount == 0:
            print 'false'
            return False
        else:
            print 'true'
            return True
        cap_lock.release()
    if mode == 'del':
        cap_lock.acquire()
        capcount += 1
        print 'true'
        return True
        cap_lock.release()
    if mode == 'max':
        cap_lock.acquire()
        if capcount == 0:
            print 'false'
            return False
        else:
            print 'true'
            return True
        cap_lock.release()
    print capcount
'''
queueing = Queue.PriorityQueue()
waitreqs = Queue.Queue()

stationName = raw_input("\nName of the station: ")
stationLocation = raw_input("City of the station: ")
streetname = raw_input("Street name of the station: ")
statcounty = raw_input("County of the station: ")
stationCapacity = int(input("Capacity of the station: "))
global_count = stationCapacity
#cap_lock = threading.Lock()

#cap_lock.acquire()

#cap_lock.release()

station = basestation(stationName, stationLocation,streetname,statcounty, stationCapacity)
data = {'id':station.id, 'name':station.name, 'street':streetname,'county':statcounty, 'location':station.location, 'capacity':station.capacity, 'time':time.time()}
postdata(data,"basestation",waitreqs)
print "Connected, Base station: "+stationName+" activated\n"

x = raw_input('Press Enter to generate mock mobile connections: ')

threads = []
thread1 = myThread('connect',queueing,waitreqs)
thread2 = myThread('disconnect',queueing,waitreqs)
thread3 = myThread('memoryreqs',queueing,waitreqs)

threads.append(thread1)
threads.append(thread2)
threads.append(thread3)

thread3.start()
thread1.start()
time.sleep(2)
thread2.start()

while 1:
    #x = raw_input('\nEnter Stop to End: ')
    print global_count
    time.sleep(1)
    if x == 'stop':
        url3 = 'basestation/'+str(station.id)
        print url3
        deletdata(url3,waitreqs)
        for activethreads in threads:
            activethreads.termination()
        break
    elif x == 'startpause':
        for activethreads in threads:
            activethreads.startpause()

thread1.join()
thread2.join()
thread3.join()

print 'End'
'''

connection("Process1",queueing,5)
disconnection("Process2",queueing)


thread.start_new_thread( connection, ("cthread1", queueing, ))
thread.start_new_thread( disconnection, ("dthread1", queueing, ))
time.sleep(4)


print 'finish'
#exitFlag = True





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
'''



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
