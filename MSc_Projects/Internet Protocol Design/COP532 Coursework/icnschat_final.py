import icns,sys,os,threading,Queue,time,socket,struct,random,math

FLAG = 1

class Reliability:
    def __init__(self):
        self.packetIDlist = range(256)
        self.existList = []
        self.messagesq = {}

    def segmentation(self,data):
        segnum = math.ceil(len(data)/94.0)
        listdata = []
        if segnum > 1:
            for i in range(int(segnum)):
                newdata = data[0:94]
                listdata.append(newdata)
                data = data[94:]
        else:
            listdata.append(data)

        return listdata

    def Encapsulate(self,format1,listdata): #
        messageID = random.choice(list(set(self.packetIDlist)-set(self.existList)))
        listlen = len(listdata)
        self.existList.append(messageID)
        self.messagesq[int(messageID)] = range(0,listlen)
        output = []
        for i in range(listlen):
            ack = 0
            if i == listlen-1:
                end = 1 << 6
            else:
                end = 0

            if format1 == "f":
                port = 1
            elif format1 == "r":
                port = 2
            else:
                port = 0  # normal

            field = ack|end|port
            header = struct.pack('!BBB',field, messageID, i)
            newData = header + listdata[i]
            output.append(newData)
        return messageID,output

    def Decapsulate(self,data):
        header = struct.unpack('!BBB',data[0:3])
        # change
        return header[0], header[1], header[2], data[3:]

    def generatedac(self,f, messid,seq, data):
        flag = f | 128
        header = struct.pack('!BBB',flag, messid ,seq)
        newData = header + data
        return newData

class Forwarding:
    # Group B 8 as example
    def __init__(self, n, s, ft, lt): # lt, ft default None, si default 8
        # 11
        self.LookupTable = lt
        self.ForwardingTable = ft
        self.hextoip = n.neighbours
        self.iptohex = n.sockaddrs
        self.source = s
    # neighbour (in number 0-15 string) and data (packet from RE layer) from Reliability layer
    def Encapsulatelist(self,dest,data):
        output = []
        for item in data:
            sour = self.source << 4
            header = sour | dest
            newdata = struct.pack('!B', header) + item
            output.append(newdata)
        return output

    def Encapsulate(self,dest,data):
        sour = self.source << 4
        header = sour | dest
        newdata = struct.pack('!B', header) + data
        return newdata

    def generatedest(self,neigh,eq,data):
        checkdest = data[0]
        eq.put(checkdest)
        if checkdest == "/":
            checkformat = data[1]
            slist = data.split(' ', 1)
            if checkformat == "f":
                dest = int(slist[0][2:])
                mesg = slist[1]
                format1 = "f"
            elif checkformat == "r":
                dest = 15
                mesg = slist[1]
                format1 = "r"
            else:
                dest = int(slist[0][1:])
                mesg = slist[1]
                format1 = "m"
        else:
            if neigh != 15:
                dest = self.getglobal(neigh)
            else:
                dest = neigh
            mesg = data
            format1 = "m"
        return dest, format1, mesg

    def getdest(self,data):
        header = struct.unpack('!B', data[0])
        source = header[0] >> 4
        dest = header[0] & 15
        return dest

    def checkdest(self,dest):
        if dest == self.source:
            return True
        elif dest == 15:
            return True
        else:
            return False

    def Decapsulate(self,data):
        header = struct.unpack('!B', data[0])
        source = header[0] >> 4
        dest = header[0] & 15
        return source, dest, data[1:]

    def getnextdigest(self,dest):
        nexthop = self.ForwardingTable[dest]
        tup = self.LookupTable[nexthop]
        hexdegest = self.iptohex[tup]
        return hexdegest

    def getglobal(self,hexd):
        tup = self.hextoip[hexd]
        for gaddr,iaddr in self.LookupTable.iteritems():
            if iaddr == tup:
                dest = gaddr
        return dest

class checksum:
    def __init__(self):
        pass

    def add_checksumlist(self, packets):
        output = []
        for packet in packets:
            checksum = 0
            toalsum = 0
            for x in packet[4:]:
                tup = struct.unpack('!B', x)
                checksum += int(tup[0])
            totalsum = checksum
            checksum = checksum & 255
            leng = len(packet)-4
            header = struct.pack('!BB', checksum,leng)
            new_packet = header + packet
            output.append(new_packet)
        return output, totalsum

    def add_checksum(self,length,packet):
        checksum = 0
        for x in packet[4:]:
            tup = struct.unpack('!B', x)
            checksum += int(tup[0])
        checksum = checksum & 255
        leng = len(packet)-4
        header = struct.pack('!BB', checksum,leng)
        new_packet = header + packet
        return new_packet


    def getlength(self, packet):
        data = struct.unpack('!B',packet[1])
        length = data[0]
        return length


    def check_checksum(self, packet):
        data = struct.unpack('!BB', packet[0:2])
        length = data[1]
        check = data[0]
        total = 0
        for x in packet[6:length+6]:
            tup = struct.unpack('!B', x)
            total += int(tup[0])
        total = total & 255

        if check == total:
            return True
        else:
            return False


class packettime(object):
    def __init__(self,num,num2,hexde,data,time):
        self.messid = num
        self.seqnum = num2
        self.data = data
        self.dest = hexde
        self.time = time
        self.count = 0


# Sender
class myThread1(threading.Thread):
    def __init__(self,n,sq,tq,eq,re,fd,ck,neigh=15):
        threading.Thread.__init__(self)
        self.sendq = sq
        self.neigh = neigh
        self.timeq = tq
        self.queue = eq
        self.re = re
        self.fd = fd
        self.ck = ck
        self.running = True

    def run(self):
        while self.running:
            while not self.sendq.empty():
                next_job = self.sendq.get()
                # self.queue.put('Data in Thread 1')
                dest, type1, data = self.fd.generatedest(self.neigh,self.queue,next_job)
                #####3
                '''
                isum = 0
                for x in data:
                    tup = struct.unpack('!B', x)
                    isum += int(tup[0])
                self.queue.put('Data sum: '+str(isum))
                '''
                ######
                #self.queue.put('Destination for this data is '+str(dest))
                self.queue.put('Destination for this data is '+str(dest))
                jobs = self.re.segmentation(data)
                self.queue.put('Separated data into '+str(len(jobs))+' segments')
                mesgid, jobs = self.re.Encapsulate(type1,jobs)
                self.queue.put('MessageID: '+str(mesgid))
                jobs = self.fd.Encapsulatelist(dest,jobs)
                jobs, totalsum = self.ck.add_checksumlist(jobs)
                # self.queue.put('total sum: '+str(totalsum))
                newneigh = self.fd.getnextdigest(dest)

                for i in range(len(jobs)):
                    n.send(str(newneigh),jobs[i])

                for i in range(len(jobs)):
                    self.queue.put('sentjob: '+str(i))
                    item = packettime(int(mesgid),i,newneigh,jobs[i],time.time())
                    self.timeq.put(item)
                    self.queue.put('item'+str(i)+' in timeq')
                self.queue.put('-----------------------------------------------------------------')

    def stop(self):
        self.running = False


# Receiver
class myThread2(threading.Thread):
    def __init__(self,n,rev,eq,re,fd,ck,neigh='0'):
        threading.Thread.__init__(self)
        self.neigh = neigh
        self.recv = rev
        self.queue = eq
        self.re = re
        self.fd = fd
        self.ck = ck
        self.running = True
        self.buffer = {}

    def run(self):
        while self.running:
            while not self.recv.empty():
                recv_data = self.recv.get()
                # self.queue.put('received somthing')
                if not self.ck.check_checksum(recv_data):
                    self.queue.put('Corrupted packet dropped')
                else:
                    self.queue.put('Packet not Corrupted')
                    length = self.ck.getlength(recv_data)
                    packetdest = self.fd.getdest(recv_data[2:])
                    self.queue.put('Received a packet, destination: '+str(packetdest))
                    if self.fd.checkdest(packetdest):
                        self.queue.put('Destination is here')
                        source, dest, data1 = self.fd.Decapsulate(recv_data[2:])
                        flags, messageid, seqnum, data2 = self.re.Decapsulate(data1)
                        self.queue.put('Decapsulated messageid: '+str(messageid)+' seqnum: '+str(seqnum))
                        if (flags & 128) >> 7: #acknowledgment packet
                            self.queue.put('Obtained an acknowledgment packet')
                            try:
                                self.re.messagesq[messageid].remove(seqnum)
                            except:
                                self.queue.put('The packet has been acked')
                            time.sleep(1)
                        else:
                            adata = self.re.generatedac(flags,messageid, seqnum, data2[:length])
                            acdata = self.fd.Encapsulate(source,adata)
                            outdata = self.ck.add_checksum(length,acdata)
                            self.queue.put('Generated Acknowledgment for messageid: '+str(messageid))
                            nextneigh = self.fd.getnextdigest(int(source))
                            self.queue.put('Nextneigh: '+str(nextneigh))
                            n.send(str(nextneigh),outdata)
                            self.queue.put('Sent Achnowledgement packet')

                            if (flags & 15) == 0:
                                if packetdest == 15:
                                    nosend = self.fd.getnextdigest(packetdest)
                                    data = self.fd.Encapsulate(15,data1)
                                    outdata = self.ck.add_checksum(length,data)
                                    for key in n.neighbours.keys():
                                        if key != nosend:
                                            n.send(key,outdata)
                                            self.queue.put('Sent Flooding message to '+str(n.neighbours[key]))

                                if not self.buffer.has_key(messageid):
                                    self.buffer[messageid] = [[-1,0,0]]
                                if (flags & 64) >> 6:
                                    self.buffer[messageid][0][1] = 1
                                tup = [seqnum,data2,length]
                                same = False
                                for item in self.buffer[messageid]:
                                    if tup[0] == item[0]:
                                        same = True
                                if not same:
                                    self.buffer[messageid].append(tup)

                                if (self.buffer[messageid][0][1] == 1 and self.buffer[messageid][0][2] == 0):
                                    if self.buffer[messageid][-1][0] == len(self.buffer[messageid])-2:
                                        data = ''
                                        self.buffer[messageid].sort(key=lambda tup: tup[0])
                                        for i in range(1,len(self.buffer[messageid])):
                                            length1 = self.buffer[messageid][i][2]
                                            data = data + str(self.buffer[messageid][i][1][:length1])
                                        self.queue.put('Message From Node ' + str(source) +' : '+ str(data))
                                        self.buffer[messageid][0][2] = 1
                                        #start timer
                                        #delete after tsendqimer
                    else:
                        nextneigh = self.fd.getnextdigest(packetdest)
                        n.send(nextneigh,recv_data)
                        self.queue.put('Passed packet to nexthop')
                self.queue.put('-----------------------------------------------------------------')
    def stop(self):
        self.running = False


class myThread3(threading.Thread):
    def __init__(self,n,tq,eq,re,neigh='0'):
        threading.Thread.__init__(self)
        self.neigh = neigh
        self.timeq = tq
        self.queue = eq
        self.re = re
        self.running = True

    def run(self):
        while self.running:
            while not self.timeq.empty():
                save_pack = self.timeq.get()
                resend = True
                ctime = time.time()-save_pack.time
                if ctime < 0.5:
                    self.timeq.put(save_pack)
                    time.sleep(0.5)
                else:
                    #self.queue.put('Start Time Check')
                    ackbool = True

                    for ip in self.re.messagesq[int(save_pack.messid)]:
                        if save_pack.seqnum == ip:
                            ackbool = False
                            self.queue.put('Have not Receive the acknowledgment for messageid: '+str(save_pack.messid)+' seq :'+str(save_pack.seqnum))
                            break
                    if ackbool:
                        self.queue.put('Received the acknowledgment for messageid: '+str(save_pack.messid)+' seq :'+str(save_pack.seqnum))
                        resend = False

                    if resend:
                        self.queue.put('Resent messageid: '+str(save_pack.messid)+' seq :'+str(save_pack.seqnum))
                        if save_pack.count < 4:
                            n.send(save_pack.dest,save_pack.data)
                            save_pack.time = time.time()
                            save_pack.count += 1
                            self.timeq.put(save_pack)
                        else:
                            self.queue.put('Finish resending 5 times')
            try:
                for key in self.re.messagesq.keys():
                    if not self.re.messagesq[int(key)]:
                        del self.re.messagesq[int(key)]
                        self.re.existList.remove(int(key))
                        self.queue.put('Received all Acknowledgment for messageid: '+str(key))
            except:
                pass

    def stop(self):
        self.running = False


class myThread4(threading.Thread):
    def __init__(self,n,ui,eq):
        threading.Thread.__init__(self)
        self.queue = eq
        self.running = True

    def run(self):
        while self.running:
            while not self.queue.empty():
                getoutput = self.queue.get()
                ui.addline(getoutput)

    def stop(self):
        self.running = False

sendq = Queue.Queue()
recvq = Queue.Queue()
timeq = Queue.Queue()
outq = Queue.Queue()


host = sys.argv[1]
n = icns.Network(int(host),0,0)
ownip = socket.gethostbyname(socket.gethostname())
ReLayer = Reliability()
if int(host) == 0:
    FTable = {0:0, 1:1, 2:1, 3:1, 8:1, 9:1, 10:1, 11:1}
    ahost = [1]
    temp = n.add_neighbour('131.231.115.27', 1)
if int(host) == 8:
    FTable = {0:1, 1:1, 2:11, 3:11, 8:8, 9:11, 10:10, 11:11}
    ahost = [1,10,11]
    temp = n.add_neighbour('131.231.115.27', 1)
    temp = n.add_neighbour('131.231.115.188', 10)
    temp = n.add_neighbour('131.231.115.38', 11)
if int(host) == 9:
    FTable = {0:2, 1:2, 2:2, 3:2, 8:2, 9:9, 10:2, 11:2}
    ahost = [2]
    temp = n.add_neighbour('131.231.114.78', 1)
if int(host) == 10:
    FTable = {0:8, 1:8, 2:8, 3:8, 8:8, 9:8, 10:10, 11:8}
    ahost = [8]
    temp = n.add_neighbour('131.231.114.128', 8)
if int(host) == 11:
    FTable = {0:8, 1:8, 2:2, 3:2, 8:8, 9:2, 10:8, 11:11}
    ahost = [2,8]
    temp = n.add_neighbour('131.231.114.78', 1)
    temp = n.add_neighbour('131.231.114.128', 8)

lookup = {0: ('131.231.115.117',0+10100), 1: ('131.231.115.27',1+10100),
          2: ('131.231.114.78',1+10100), 3: ('131.231.114.126',1+10100),
          8: ('131.231.114.128',8+10100), 9: ('131.231.114.82',1+10100),
         10: ('131.231.115.188',10+10100), 11: ('131.231.115.38',11+10100)}  # {(IP, PORT): number}
FdLayer = Forwarding(n,int(host),FTable,lookup)
CkLayer = checksum()

while 1:
    print 'Main Menu'
    sel = input('1. Enter Chat Room \n2. Show Neighbours\n3. End Program\n')
    if sel == 1:
        print 'Avaliable hosts : ',ahost
        host = raw_input('Select default host: ')
        key = lookup[int(host)]
        temp = n.sockaddrs[key]
        print temp
        time.sleep(3)
        ui = icns.UI('Chat Room')
        send = myThread1(n,sendq,timeq,outq,ReLayer,FdLayer,CkLayer,temp)
        recv = myThread2(n,recvq,outq,ReLayer,FdLayer,CkLayer,temp)
        timeout = myThread3(n,timeq,outq,ReLayer,temp)
        outscreen = myThread4(n,ui,outq)
        send.start()
        recv.start()
        timeout.start()
        outscreen.start()
        while 1:
            data = ui.getfd()
            r = n.orfd(data)
            if r == 1:
                data = os.read(data,1000)
                if data == '/stop':
                    break
                elif data == '/show neighbour':
                    outq.put(n.neighbours)
                    outq.put(n.sockaddrs)
                else:
                    outq.put('Me: '+data)
                    sendq.put(data)
            elif r == 2:
                data = n.receive()
                recvq.put(data[0])

        ui.stop()
        send.stop()
        send.join()
        recv.stop()
        recv.join()
        timeout.stop()
        timeout.join()
        outscreen.stop()
        outscreen.join()
        print 'Chat Window closed.'
    elif sel == 2:
        print "List of Neighbours:"
        for haddr,iaddr in n.neighbours.iteritems():
            print "IP Address: %s, Network: %d "%(iaddr[0],int(iaddr[1]-10100))
            print "hexdigest : %s "%(str(haddr))

        print n.neighbours
        print n.sockaddrs

    elif sel == 3:
        print 'end program'
        break
