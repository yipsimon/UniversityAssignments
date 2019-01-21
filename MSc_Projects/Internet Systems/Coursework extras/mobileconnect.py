import thread, json, Queue
import time, random, traceback
from socket import socket, AF_INET, SOCK_STREAM

#basestations = ["Loughborough-1","Leicester-1"]
#,"Nottingham-1","Loughborough-2"]
#dicbasestation = {"Loughborough-1":1234,"Leicester-1":9999}
#,"Nottingham-1":5002,"Loughborough-2":5003

f = open('ports.txt','r')
stations = []
portnumber = {}
for x in f.readlines():
	y = x.split()
	print y
	stations.append(y[0])
	portnumber[y[0]] = int(y[1])
f.close()


class mobile():
	def __init__(self):
		self.number = '07' + ''.join(["%s" % random.randint(0, 9) for num in range(0, 9)])
		self.conlimit = random.randint(5, 60)
		self.loc = random.choice(stations)
		print "Mobile: "+str(self.number)+", Connection to "+self.loc+"\n"
	
	def connect(self):
		self.port = portnumber[self.loc]
		self.s = socket(AF_INET,SOCK_STREAM)
		self.s.connect(("127.0.0.1",self.port))
		print "Connected to base station "+self.loc+", Port :"+str(self.port)+"\n"
		
	def send(self):
		data = {'Number':self.number,'Message':'Hello'}
		data_string = json.dumps(data) #data serialized
		self.s.send(data_string)
		resp=self.s.recv(1024)
		return resp
	
	def stopcon(self):
		data = {'Number':self.number,'Message':'Bye'}
		data_string = json.dumps(data) #data serialized
		self.s.send(data_string)
		resp=self.s.recv(1024)
		return resp

	def close(self):
		self.s.close()

#queueLock = thread.Lock()
#data_loaded = json.loads(data) #data loaded
def connection(threadname, list):
	i = 0
	while i < 5:
		newconnect = mobile()
		newconnect.connect()
		reply = newconnect.send()
		print reply
		#list.append(newconnect)
		i += 1
		#print "%s: %d" % ( threadname, 1)
		newconnect.close()
		#time.sleep(1)


		
def disconnection(threadname, list):
	time.sleep(8)
	while len(list) > 0:
		print str(len(list))
		num = random.randint(0,len(list)-1)
		print num
		time.sleep(random.randint(0,5))
		#closing = list[num].send('Exit')
		#print closing
		list[num].close() 
		#queueLock.acquire()
		list.pop(num)
		
		#queueLock.release()
	
list = []
'''
i = 0
while i < 4:
	newconnect = mobile()
	newconnect.connect()
	reply = newconnect.send('Hello')
	print reply
	#queueLock.acquire()
	list.append(newconnect)
	#queueLock.release()
	i += 1
	time.sleep(1)

while len(list) > 0:
	print len(list)
	num = random.randint(0,len(list)-1)
	print num
	time.sleep(random.randint(0,5))
	closing = list[num].send('Exit')
	print closing
	list[num].close() 
	#queueLock.acquire()
	list.pop(num)
	time.sleep(1)

'''
thread.start_new_thread( connection, ("conthread", list, ))
#thread.start_new_thread( disconnection, ("disthread", list, ))

'''
class Job(object):
    def __init__(self, priority, description):
        self.priority = priority
        self.description = description
    def __cmp__(self, other):
        return cmp(self.priority, other.priority)

q = Queue.PriorityQueue()

q.put( Job(3, 'Mid-level job') )
q.put( Job(10, 'Low-level job') )
q.put( Job(1, 'Important job') )

while not q.empty():
    next_job = q.get()
    print 'Processing job:', next_job.description
'''

#try:
	
#except:
#	print "Error: unable to start thread"


#for socket in connectlist:
#	socket.close()
#	print 'Closed '+str(socket.number)
