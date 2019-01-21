import time, random, traceback, uuid, calendar, sys, requests, json, Queue, numpy

def getdata(dir):
    url = "http://cosyly@sci-project:5001/"+str(dir)
    count = 5
    while count:
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.exceptions.ConnectionError as e:
            print e
            print "Connection error: retrying in 3 seconds..."
            count -= 1
            time.sleep(3)
        except requests.exceptions.HTTPError as err:
            print err
            print "http requests error", response.status_code
            print "Failed to get data, retrying in 3 seconds..."
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
while True:
    print '\nOption 1: Show a list of Base Stations'
    print 'Option 2: List of the busiest Base Stations'
    print 'Option 3: Get current mobile connections by station ID (choose 1 to get station ID for input)'
    print 'Option 4: Get Base Stations grouped by location'
    print 'Option 5: Get statistics'
    print 'Option 7: Termination'

    x = input("Select: ")
    if x == 1:
        data = getdata("basestation")
        records = json.loads(data)
        #data.split('},')
        for i in range(len(records)):
            print "\nStation ID: \t\t%s,\
            \nStation Name: \t\t%s,\
            \nStation Capacity: \t%d,\
            \nStreet: \t\t%s,\
            \nCity: \t\t\t%s,\
            \nCounty: \t\t%s" % (records[i]['stationid'],records[i]['stationname'],records[i]['capacity'],records[i]['street'], records[i]['location'], records[i]['county'])

            print "Time started: \t\t", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(records[i]['timestarted']))
    elif x == 2:
        data = getdata("basestation/busy")
        records = json.loads(data)

        for i in range(len(records)):
            print "\nStation ID: \t\t%s,\
            \nStation Name: \t\t%s,\
            \nStation Capacity: \t%d,\
            \nStreet: \t\t%s,\
            \nCity: \t\t\t%s,\
            \nCounty: \t\t%s" % (records[i]['stationid'],records[i]['stationname'],records[i]['capacity'],records[i]['street'], records[i]['location'], records[i]['county'])

            print "Time started: \t\t", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(records[i]['timestarted']))
    elif x == 3:
        choice = raw_input("\nPlease input a station ID: ")
        url = "basestation/getid/" + str(choice)
        choice_data = getdata(url)
        records = json.loads(choice_data)
        if len(records) == 0:
            print "The inputted station ID does not exist in the database."
        else:
            for i in range(len(records)):
                print "\nStation ID : \t\t%s,\
                \nPhone number: \t\t%s,\
                \nMessage: \t\t%s" % (records[i]['stationid'], records[i]['number'], records[i]['message'])

                print "Time of connection: \t", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(records[i]['timeofconnection']))
    elif x == 4:
        choice = raw_input("\nPlease input a city/location: ")
        url = "basestation/getloc/" + str(choice)
        choice_data = getdata(url)
        records = json.loads(choice_data)
        if len(records) == 0:
            print "Base stations do not exist within the area of the inputted location"
        else:
            for i in range(len(records)):
                print "\nStation ID: \t\t%s,\
                \nStation Name: \t\t%s,\
                \nStation Capacity: \t%d,\
                \nStreet: \t\t%s,\
                \nCity: \t\t\t%s,\
                \nCounty: \t\t%s" % (records[i]['stationid'],records[i]['stationname'],records[i]['capacity'],records[i]['street'], records[i]['location'], records[i]['county'])

                print "Time started: \t\t", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(records[i]['timestarted']))
    elif x == 5:
        url = "basestation/stat"
        choice_data = getdata(url)
        records = json.loads(choice_data)
        cap = []
        for i in range(len(records)):
            print "\nStation ID: \t\t%s,\
            \nStation Name: \t\t%s,\
            \nStation Capacity: \t%d,\
            \nCurrent number of connection: \t\t%s,\
            \nPercentage of used capacity: \t\t%s,\
            " % (records[i]['stationid'],records[i]['stationname'],records[i]['capacity'],records[i]['connected'], records[i]['percent'])
            cap.append(records[i]['connected'])

        a = numpy.array(cap)
        cmean = numpy.mean(a)
        print 'Average number of connection across all base stations is '+str(cmean)+'\n'

    elif x == 7:
        sys.exit(1)
    else:
        print "Error: Please input valid option."
