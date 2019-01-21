import threading, time, random, traceback, uuid, requests, json, Queue, sys

threadLock = threading.Lock()
global_count = 0

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
        if global_count == -1:
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
        self.conlimit = random.randint(1, 9)
        self.loc = station.location

    def connect(self,mess,q):
        self.data = {'number':self.number,'message':mess,'timeofconnection':time.time(),'stationid':station.id}
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
    url = "http://cosyly@sci-project:5001/"+str(dir)
    payload = json.dumps(data)
    count = 5
    while count:
        try:
            r = requests.post(url, payload)
            r.raise_for_status()
            subt_count()
            break
        except requests.exceptions.ConnectionError as e:
            print e
            print "connection error, fall to send data"
            if dir == 'basestation':
                count -= 1
            else:
                q.put(failreq('post',data,dir))
                time.sleep(5)
                break
        except requests.exceptions.HTTPError as err:
            print err
            print "http requests error",r.status_code
            print "fail to send data"
        except requests.exceptions.RequestException as error:
            print error
            print "Fatal Error Terminating"
            sys.exit(1)
    if count == 0:
        print 'Fatal Error Terminating'
        sys.exit(1)


def deletdata(dir,q):
    url = "http://cosyly@sci-project:5001/"+str(dir)
    try:
        r = requests.delete(url)
        r.raise_for_status()
        add_count()
    except requests.exceptions.ConnectionError as e:
        print e
        print "connection error, fall to send data"
        q.put(failreq('del',dir,dir))
        time.sleep(5)
    except requests.exceptions.HTTPError as err:
        print err
        print "http requests error",r.status_code
        print "fail to send data"
    except requests.exceptions.RequestException as error:
        print error
        print "Fatal Error Terminating"
        sys.exit(1)

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
                elif not self.count:
                    time.sleep(2)

        if self.mode == 'disconnect':
            time.sleep(8)
            while self.run1:
                while not self.q.empty():
                    next_job = self.q.get()
                    wait = next_job.conlimit
                    if self.quit:
                        wait = 0
                    time.sleep(wait)
                    next_job.disconnect(self.errq)


        if self.mode == 'memoryreqs':
            while self.run1:
                while not self.errq.empty():
                    self.count = check_count()
                    job = self.errq.get()
                    if job.type == 'post':
                        if self.count:
							temp = mobile()
							postdata(job.data,job.dir,self.errq)
							temp.number = job.data['number']
							self.q.put(temp)
                        else:
                            self.errq.put(job)
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
        self.quit = True
        if self.mode == 'disconnect':
            while not self.q.empty():
                pass
            print 'Main queue is empty'
        if self.mode == 'memoryreqs':
            while not self.errq.empty():
                pass
            print 'Error queue is empty'
        self.run1 = False

queueing = Queue.PriorityQueue()
waitreqs = Queue.Queue()
stationName = raw_input("\nName of the station: ")
stationLocation = raw_input("City of the station: ")
streetname = raw_input("Street name of the station: ")
statcounty = raw_input("County of the station: ")
while True:
    try:
        stationCapacity = int(input("Capacity of the station: "))
        break
    except:
        print 'Enter a number'

global_count = stationCapacity

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
    x = raw_input('\nEnter stop to End: ')
    if x == 'stop':
        url3 = 'basestation/'+str(station.id)
        #print url3
        deletdata(url3,waitreqs)
        for activethreads in threads:
            activethreads.termination()
        break
    elif x == 'start' or 'pause':
        for activethreads in threads:
            activethreads.startpause()

thread1.join()
thread2.join()
thread3.join()

print 'End'
