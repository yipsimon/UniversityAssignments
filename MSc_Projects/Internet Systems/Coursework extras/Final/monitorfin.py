import time, random, traceback, uuid, calendar
import requests
import json
import Queue
import bson.json_util

def getdata(dir):
    #url = "http://127.0.0.1:5001/basestation"
    #url = "http://cosyly@sci-project:5001/basestation" working
    #url = "http://cosyly@sci-project.lboro.ac.uk:8080/todo/ap7/v1.0/tasks/"+dir
    #url = "http://cosyly@sci-project:5001/"+str(dir)
    url = "http://127.0.0.1:5001/"+str(dir)
    count = 5
    while count:
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.exceptions.ConnectionError as e:
            print e
            print "connection error, retry in 3 seconds"
            count -= 1
            time.sleep(3)
        except requests.exceptions.HTTPError as err:
            print err
            print "http requests error",response.status_code
            print "fail to get data, retry in 3 seconds"
            count -= 1
            time.sleep(3)
        except requests.exceptions.RequestException as error:
            print error
            print "Fatal Error Terminating"
            sys.exit(1)
        if response.status_code == 200:
            return response.content
    print 'unable to get data '


print 'Network Monitoring Application'
print 'Option 1: Show a list of Base Stations'
print 'Option 2: a list of busiest Base Stations'
while True:
    x = input("Select :")
    if x == 1:
        data = getdata("basestation")
        print data
        tests = json.loads(data)
        #data.split('},')
        for test in tests:
            print test
            print 'hello'
            print test['stationname']
            print 'bye'
        for i in range(len(tests)):
            print "stationid: %s, stationname: %s, capacity: %d, location: %s, street: %s, county: %s" % (tests[i]['stationid'],tests[i]['stationname'],tests[i]['capacity'],tests[i]['location'],tests[i]['street'],tests[i]['county'])
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(tests[i]['timestarted']))
    if x == 2:
        data = getdata("basestation/busy")
        print data
        tests = json.loads(data)
        #data.split('},')
        for test in tests:
            print test
            print 'hello'
            print test['stationname']
            print 'bye'
            '''
        for i in range(len(tests)):
            print "stationid: %s, stationname: %s, capacity: %d, location: %s, street: %s, county: %s" % (tests[i]['stationid'],tests[i]['stationname'],tests[i]['capacity'],tests[i]['location'],tests[i]['street'],tests[i]['county'])
            print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(tests[i]['timestarted']))
        '''
        '''
        data = json.loads(data)
        for doc in data:
            output.append(doc)

        i = 0
        for item in output:
            print str(i)+" "+item+'\n'
            i += 1
        '''
