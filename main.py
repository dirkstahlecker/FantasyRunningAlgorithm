#my userid: 852f946a-79d8-4cd0-8ced-eea41e78725b

import urllib2
import json

################ constants ###############################################
TIER1_DURATION = 60
TIER2_DURATION = 40
TIER3_DURATION = 20

TIER1_SPEED = 8
TIER2_SPEED = 4
TIER3_SPEED = 2

NUM_PAGES = 35

################ methods ###############################################
def makeRequest(page):
    req = urllib2.Request('https://pumatrac-geo-api.herokuapp.com/activities?bounds=box:0,0:90,180&page=' + str(page)) #get all data
    req.add_header('Authorization', 'Bearer 1cfb51cd69904221818dafc4069f9d61')
    resp = urllib2.urlopen(req)
    content = resp.read()
    decoded_json = json.JSONDecoder().decode(content)
    return decoded_json

#initialize list holders
duration_list = []
mean_speed_list = []
tier1_count = tier2_count = tier3_count = 0

def addToLists(decoded_json):
    for activity in decoded_json['activities']:
        if activity['mode'] != 'outdoor' and activity['mode'] != 'treadmill': #ignore exercise that isn't running
            continue

        duration = activity['duration']
        duration = float(duration) / 60; #convert to minutes
        duration_list.append(duration)
        mean_speed = activity['mean_speed']
        mean_speed_list.append(mean_speed)

def doAnalytics():
    #average of each
    print 'Average duration: ',
    duration_avg = float(sum(duration_list)) / len(duration_list)
    print duration_avg
    print 'Average mean speed ',
    mean_speed_avg = float(sum(mean_speed_list)) / len(mean_speed_list)
    print mean_speed_avg

################ execution ###############################################

#populate the lists from the API data
for x in range(0,NUM_PAGES):
    addToLists(makeRequest(x))

doAnalytics()

#print duration_list
#print mean_speed_list


#utilize distance, duration, mean speed



