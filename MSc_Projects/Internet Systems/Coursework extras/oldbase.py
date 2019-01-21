import random, json, time, threading, Queue, traceback, datetime

exitFlag = 0

class mobile(object):
        def __init__(self):
                self.number = "07508"+str(random.randint(100000, 999999))
                #self.conlimit = random.randint(60, 900)
                self.loc = random.choice(basestations)
                print "Mobile: "+str(self.number)+", Connection to "+self.loc+"\n"

class myBase(threading.Thread):
        def __init__(self,id,location,cap,q):
                threading.Thread.__init__(self)
                self.id = id
                self.loc = location
                self.capacity = cap
                self.timestarted = str(time.time())
                self.q = q
                #payload = {'id':self.id,'location':self.loc, 'capacity':self.cap, 'start time':self.timestarted}
                #r = requests.post(url, data=payload)
                
        def run(self):
                print "Starting base station: "+self.loc+" ID: "+str(self.id)+"\n"
                #Send Base station data to server
                
                #Get mobile data 
                #queueLock.acquire()
                #print "Starting " + str(self.id)+"\n"
                processdata(self.id,self.q)
                
                #queueLock.release()
                
        def __str__(self):
                return "{} {} {} {}".format(self.id,self.loc,self.cap,self.timestarted)
'''
def check_data(baselocation, queue):
        getqueue = queue.get()
        if baselocation = getqueue.loc:
                json_data = json.dumps(getqueue)
                send_data(json_data)
             
			 q.task_done()
        else:
                q.task_done()
                queue.append(getqueue)
'''     
                
def processdata(baseid,withqueue):
        while not exitFlag:
                queueLock.acquire()
                #if not queueList[baseid-1].empty():
                data = withqueue.get()
                queueLock.release()
                print "%d processing %d\n" % (baseid, data.number)
                print "Processed "+str(data.number)+"\n"
                #else:
                #        queueLock.release()
                #        print "No Data "+str(baseid)+"\n"
                #        time.sleep(1)
        #mdata = {'number':temp.number, 'starttime':time.time(), 'Connection':temp.loc}
        #data = {a}
        
        #       s.send(json_data)       
                
                
basestations = ["Loughborough-1","Leicester-1","Nottingham-1","Loughborough-2"]
capacitylist = [20,10,20,10]
queueLock = threading.Lock()
workQueue1 = Queue.Queue(20)
workQueue2 = Queue.Queue(10)
workQueue3 = Queue.Queue(20)
workQueue4 = Queue.Queue(10)
threads = []

runloop = True
uniqueid = 1


for base in basestations:
        numcap = capacitylist[uniqueid-1]
		name = workQueue+str(uniqueid)
        thread = myBase(uniqueid,base,numcap,name)
        #worker.setDaemon(True)
        thread.start()
        threads.append(thread)
        uniqueid += 1   
#Generate mobile data and fill the queue

while runloop:
        a = mobile()
        queueLock.acquire()
        ind = basestations.index(a.loc)
        queueList[ind].put(a)
        queueLock.release()
        #random.choice(location)
        
        #if a.loc == 'Loughborough':
        #       data = {a}
        #       json_data = json.dumps(data)
        #       s.send(json_data)
        time.sleep(random.randint(1,4))


