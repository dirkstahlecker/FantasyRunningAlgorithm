#my userid: 852f946a-79d8-4cd0-8ced-eea41e78725b

import urllib2
import json
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
from Person import *
import yaml
import Goal

################ constants ###############################################
TIER1_DURATION = 60
TIER2_DURATION = 40
TIER3_DURATION = 20

TIER1_SPEED = 8
TIER2_SPEED = 4
TIER3_SPEED = 2

NUM_PAGES = 50
MIN_DURATION = 10 #minutes
MIN_DISTANCE = 0.25 #miles
MAX_DISTANCE = 200 #miles
MAX_DURATION = 20*60 #minutes

################ Get data ###############################################
def makeRequest(page):
    #TODO: error handling on pagination
    req = urllib2.Request('https://pumatrac-geo-api.herokuapp.com/activities?bounds=box:0,0:90,180&page=' + str(page))
    req.add_header('Authorization', 'Bearer 1cfb51cd69904221818dafc4069f9d61')
    resp = urllib2.urlopen(req)
    content = resp.read()
    decoded_json = json.JSONDecoder().decode(content)
    return decoded_json

#initialize list holders
duration_list = []
mean_speed_list = []
distance_list = []
tier1_count = tier2_count = tier3_count = 0


def pullStatsFromRun(activity):
    duration = activity['duration']
    duration = float(duration) / 60; #convert to minutes
    
    mean_speed = activity['mean_speed']
    distance = activity['distance']
    distance = distance * 0.621 #convert to miles

    #enforce minimums
    if duration < MIN_DURATION or distance < MIN_DISTANCE:
        return None
    #weed out unreasonable maximums
    if duration > MAX_DURATION or distance > MAX_DURATION:
        return None

    return (duration, mean_speed, distance)

people = {}
id_list = []
def addToLists(decoded_json): #this method gets called multiple times (once per page)
    ID_to_test = None
    for activity in decoded_json['activities']:
        if activity['mode'] != 'outdoor' and activity['mode'] != 'treadmill': #ignore exercise that isn't running
            continue

        try:
            (duration, mean_speed, distance) = pullStatsFromRun(activity)
            thisRun = (duration, mean_speed, distance)
        except:
            continue
        
        mean_speed_list.append(mean_speed)
        duration_list.append(duration)
        distance_list.append(distance)

        ID = activity['id']

        if ID_to_test == None:
            ID_to_test = ID
        
        #new ID
        if ID not in id_list:
            #create person and add to dictionary
            person = PersonClass(ID)
            person.addRun(thisRun)
            people[ID] = person
            id_list.append(ID)
        #seen this ID before
        else:
            #append new info to the dictionary
            people[ID].addRun(thisRun)

        return ID_to_test



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



def doAnalytics():
    #average of each
    print 'Average duration: ',
    duration_avg = float(sum(duration_list)) / len(duration_list)
    print duration_avg
    print 'Max duration: ',
    print max(duration_list)
    print 'mean_speed_list: ',
    print mean_speed_list
    mean_speed_avg = float(sum(mean_speed_list)) / len(mean_speed_list)
    print mean_speed_avg
    print 'Average distance: ',
    distance_list_avg = float(sum(distance_list)) / len(distance_list)
    print distance_list_avg
    print 'Max distance: ',
    print max(distance_list)
    print 'Min distance: ',
    print min(distance_list)



################ Score and Analyze ###############################################
def getTier(duration_list_in, mean_speed_list_in): #inputs are lists of a single person's runs
    pass


def checkGoal(goal, person):
    if True:
        return goal.completedValue()
    return 0
    #TODO: fill this in


#constants for scoring
MEAN_SPEED_DIFF_PROP_CONST = 2
DURATION_PROP_CONST = 1
DISTANCE_PROP_CONST = 1

def scoreRun(person, goal, duration_list_in, mean_speed_list_in, distance_list_in):
    score = 0
    #score += checkGoal()

    #currentRuns = person.getCurrentWeekRuns()
    currentRun = person.getMostRecentRun()[0]
    #ASSUMPTION: only look at most recent run, in place of most recent week. Week infrastructure is long and complicated
    #(duration_avg, mean_speed_avg, distance_avg) = person.getCurrentWeekAverages() 
    
    (duration_total, mean_speed_total, distance_total) = person.getTotalAverages()
    '''
    duration_diff = duration_avg - duration_total
    mean_speed_diff = mean_speed_avg - mean_speed_total
    distance_diff = distance_avg - distance_total
    '''
    duration_diff = currentRun[0] - duration_total
    mean_speed_diff = currentRun[1] - mean_speed_total
    distance_diff = currentRun[2] - distance_total

    score += duration_diff * MEAN_SPEED_DIFF_PROP_CONST
    score += mean_speed_diff * MEAN_SPEED_DIFF_PROP_CONST
    score += distance_diff * DISTANCE_PROP_CONST

    print 'Score: ',
    print score

    return score
    


def graphList():
    data = mean_speed_list
    mu, std = norm.fit(data)
    plt.hist(data, bins=25, normed=True, alpha=0.6, color='g')

    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    p = norm.pdf(x, mu, std)
    plt.plot(x, p, 'k', linewidth=2)
    title = "Fit results: mu = %.2f,  std = %.2f" % (mu, std)
    plt.title(title)

    plt.show()



################ execution ###############################################


def main():
    #populate the lists from the API data
    # get some new data by uncommenting this
    # saveDataToFile('data.txt', NUM_PAGES)
    #data = getDataFromFile('data.txt')
    #ID_to_test = addToLists(data)
    for x in range(0,NUM_PAGES):
        ID_to_test = addToLists(makeRequest(x))

    doAnalytics()
    graphList()
    '''
    req = urllib2.Request('https://pumatrac-geo-api.herokuapp.com/activities?bounds=box:0,0:90,180&page=0')
    req.add_header('Authorization', 'Bearer 1cfb51cd69904221818dafc4069f9d61')
    resp = urllib2.urlopen(req)
    content = resp.read()
    #userID = content['activities'][0]['id']
    '''
    scoreRun(people[ID_to_test], None, duration_list, mean_speed_list, distance_list)

if __name__ == "__main__":
    main()




#print duration_list
#print mean_speed_list

