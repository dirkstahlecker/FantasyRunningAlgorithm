#my userid: 852f946a-79d8-4cd0-8ced-eea41e78725b

import urllib2
import json
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
from Person import *
import yaml
from Goal import *
from Run import *
from random import randint

################ constants ###############################################

NUM_PAGES = 1

################ Get data ###############################################
def makeRequest(page):
    #TODO: error handling on pagination
    req = urllib2.Request('https://pumatrac-geo-api.herokuapp.com/activities?bounds=box:74.38,72.20:41.01,40.29&mode=outdoor&page=' + str(page))
    #req = urllib2.Request('https://pumatrac-geo-api.herokuapp.com/activities?user_id=2143d242-afff-42eb-9f6d-7981b8ea170c')
    req.add_header('Authorization', 'Bearer 1cfb51cd69904221818dafc4069f9d61')
    resp = urllib2.urlopen(req)
    content = resp.read()
    #decoded_json = json.JSONDecoder().decode(content)
    decoded_json = json.loads(content)
    return decoded_json

#initialize list holders
duration_list = []
mean_speed_list = []
distance_list = []
tier1_count = tier2_count = tier3_count = 0


people = {} # { ID : person }
def addToLists(decoded_json, count): #this method gets called multiple times (once per page)
    print count #print page number for reference while running long batches
    count += 1
    for activity in decoded_json['activities']:
        mode = activity['mode']
        if mode != 'outdoor' and mode != 'treadmill': #ignore exercise that isn't running (indoor and outdoor are equivalent)
            continue

        thisRun = None
        try:
            thisRun = pullStatsFromRun(activity)
        except:
            print 'Run was None'
            continue

        if thisRun == None:
            continue

        mean_speed_list.append(thisRun.mean_speed)
        duration_list.append(thisRun.duration)
        distance_list.append(thisRun.distance)

        ID = activity['id']
        
        #new ID
        if ID not in people:
            person = None
            #create person and add to dictionary
            person = PersonClass(ID, goals_list[0])

            if len(person.weeks) != 0:
                person.weeks = {}

            person.addRun(thisRun)
            #print 'weeks after adding run: ',
            #print person.weeks
            people[ID] = person
        #seen this ID before
        else:
            #append new info to the dictionary
            people[ID].addRun(thisRun)
            print 'PREVIOUSLY SEEN ID ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'



################ File Interaction ###############################################
def saveDataToFile(file_name, num_pages):
    if num_pages == 0:
        print 'num_pages must be greater than 0'
        return

    all_data = makeRequest(0)

    for i in range(num_pages - 1):
        data = makeRequest(i + 1)
        all_data['activities'] = all_data['activities'] + data['activities']

    #add data to file
    with open(file_name, 'w') as outfile:
        json.dump(all_data, outfile)


def getDataFromFile(file_name):

    # load data from file
    with open(file_name) as data_file:
        data = yaml.load(data_file)

    return data
    # for activity in data['activities']:
    #     if activity['mode'] != 'outdoor' and activity['mode'] != 'treadmill':  # ignore exercise that isn't running
    #         continue
    #
    #     stats = pullStatsFromRun(activity)
    #     # in case stats is a NoneType
    #     if (stats):
    #         (duration, mean_speed, distance) = stats
    #         mean_speed_list.append(mean_speed)
    #         duration_list.append(duration)
    #         distance_list.append(distance)


################ Score and Analyze ###############################################
def doAnalytics():
    #average of each
    print 'Average duration: ',
    duration_avg = float(sum(duration_list)) / len(duration_list)
    print duration_avg
    print 'Max duration: ',
    print max(duration_list)
    mean_speed_avg = float(sum(mean_speed_list)) / len(mean_speed_list)
    print mean_speed_avg
    print 'Average distance: ',
    distance_list_avg = float(sum(distance_list)) / len(distance_list)
    print distance_list_avg
    print 'Max distance: ',
    print max(distance_list)
    print 'Min distance: ',
    print min(distance_list)



def getTier(duration_list_in, mean_speed_list_in): #inputs are lists of a single person's runs
    pass


def checkGoal(goal, person):
    if True:
        return goal.completedValue()
    return 0
    #TODO: fill this in



def graphList(data):
    mu, std = norm.fit(data)
    plt.hist(data, bins=25, normed=True, alpha=0.6, color='g')

    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    p = norm.pdf(x, mu, std)
    plt.plot(x, p, 'k', linewidth=2)
    #plt.plot(x,'k',linewidth=2)
    title = "Fit results: mu = %.2f,  std = %.2f" % (mu, std)
    plt.title(title)

    plt.show()



goals_list = []
#used to populate a few goals for the heirarchy
def makeGoals():
    goal = Goal(1, 15)
    goal.params['numRuns'] = 3
    goal.params['totalDuration'] = 60
    goals_list.append(goal)

    goal = Goal(2, 20)
    goal.params['runAvgSpeed'] = 10
    goal.params['totalDistance'] = 30
    goals_list.append(goal)

    goal = Goal(3, 30)
    goal.params['totalDistance'] = 60
    goal.params['runMinSpeed'] = 8
    goals_list.append(goal)


################ execution ###############################################

def doData():
    #populate the lists from the API data
    # get some new data by uncommenting this
    # saveDataToFile('data.txt', NUM_PAGES)
    #data = getDataFromFile('data.txt')
    makeGoals()
    count = 0
    for x in range(0,NUM_PAGES):
        addToLists(makeRequest(x), count)
        count += 1

#clone of doData but using data from a stored file
def doDataFromFile(filePath):
    makeGoals()

    s = open(filePath, 'r').read()
    j = json.loads(s)
    #addToLists(getDataFromFile(filePath))
    addToLists(j, 0)


#helper to get a random run and return a json string to be sent into the API
def makeJsonOfRandomRun():
    keys = people.keys()
    maxLen = len(keys)-1
    i = keys[randint(0,maxLen)]
    person = people[i]

    run = person.getMostRecentRun()
    
    return json.dumps({
        'duration': run.duration, 
        'distance': run.distance,
        'mean_speed': run.mean_speed,
        'date': str(run.date)
        })
    

# send data for the front end to utilize
# current in proof of concept mode
def sendDataToFrontEnd():
    #url = 'http://cms634fantasyrunningapp-fantasyrunning.rhcloud.com/data/addBackendDataToDatabase'
    url = 'http://localhost:6340/data/addBackendDataToDatabase'

    #data = makeJsonOfRandomRun()
    data = json.loads(people['a5da3bd1-35e3-4926-9857-d575fd3a40d3'].toJsonString())
    print 'sending data: '
    print data
    data = json.dumps({'person': data})

    req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
    f = urllib2.urlopen(req)
    response = f.read()
    print 'Successfully sent data. Response: ',
    print response
    f.close()

def makePostQuery(url, data):
    req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
    f = urllib2.urlopen(req)
    response = f.read()
    f.close()
    return response

def makeGetQuery(url):
    response = urllib2.urlopen(url).read()
    return response


#main control loop
def main():
    #saveDataToFile('data_store_10_pages', 10)
    #doData()
    doDataFromFile('onePageDirectlyFromAPIChangedIDs.txt')

    #sendDataToFrontEnd()

    #response = makeGetQuery('http://cms634fantasyrunningapp-fantasyrunning.rhcloud.com/data/runs/54862a7d-717b-44b9-a1d4-c07e190a74fd')
    #response = makeGetQuery('http://localhost:6340/data/runs/54862a7d-717b-44b9-a1d4-c07e190a74fd')
    #print 'response: ',
    #print response
    '''
    dataToSend = '{"people": ['
    for person in people:
        dataToSend += people[person].toJsonString() + ', '
    dataToSend = dataToSend[:len(dataToSend) - 2]
    dataToSend += ']}'
    
    #print dataToSend

    f = open('output.txt', 'w')
    f.write(dataToSend)

    print 'data saved to file'
    '''

    print people['73ad4cf4-95f8-4b9d-83e5-70782b54eaa1'].weeks

    for i in people:
        person = people[i]
        if person.getTotalNumberOfRuns() > 10:
            print person.getTotalNumberOfRuns()
            print person.weeks


    return 


    while True:
        #doDataFromFile()
        doData()
        print '\n\n'
        print 'Enter user ID: '
        personID = raw_input('>')
        personID = personID.strip().lstrip().lower()
        try:
            person = people[personID]
        except:
            continue

        print '(S)core run\n(V)iew statistics\nView (O)verall statistics\n(G)raph'
        inp = raw_input('>')
        inp = inp.strip().lstrip().lower()
        if inp == 's':
            #score run
            scoreRun(person, goals_list[randint(0,2)], person.getMostRecentRun())
        elif inp == 'v':
            #view stats
            print 'Number of total runs: ',
            print str(person.getTotalNumberOfRuns())
            print 'Most recent run: ',
            print person.getMostRecentRun().toString()
            print 'This week\'s goal: ',
            print person.goal.toString()
        elif inp == 'o':
            doAnalytics()
        elif inp == 'g':
            l_avg = []
            l_dist = []
            l_dur = []
            for run in person.getCurrentWeekRuns():
                l_avg.append(run.mean_speed)
                l_dist.append(run.distance)
                l_dur.append(run.duration)

            print '(A)verage speed\nD(i)stance\nD(u)ration'
            i = raw_input('>')
            i = i.strip().lstrip().lower()
            if i == 'a':
                graphList(l_avg)
            elif i == 'i':
                graphList(l_dist)
            elif i == 'u':
                graphList(l_dur)


if __name__ == "__main__":
    main()




'''
To do:
-get everyone in class on puma trac, populate weeks of data for them, then have each run 
and split into teams to simulate an actual competition
    -have a star athlete as a part of each team as well (taken from pumatrac existing data)
-possibly create graphs and send them to front end
-figure out how to get data to front end
-fix issue with runs not going to the proper people solely
-put data into database
'''