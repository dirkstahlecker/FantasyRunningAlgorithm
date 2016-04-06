
import urllib2
import json
import yaml
import pickle


NUM_PAGES = 50
MIN_DURATION = 10 #minutes
MIN_DISTANCE = 0.25 #miles
MAX_DISTANCE = 200 #miles
MAX_DURATION = 20*60 #minutes

#initialize list holders
duration_list = []
mean_speed_list = []
distance_list = []
tier1_count = tier2_count = tier3_count = 0


def makeRequest(page):
    #TODO: error handling on pagination
    req = urllib2.Request('https://pumatrac-geo-api.herokuapp.com/activities?bounds=box:0,0:90,180&page=' + str(page))
    req.add_header('Authorization', 'Bearer 1cfb51cd69904221818dafc4069f9d61')
    resp = urllib2.urlopen(req)
    content = resp.read()
    decoded_json = json.JSONDecoder().decode(content)
    return decoded_json


def pullStatsFromRun(activity):
    duration = activity['duration']
    duration = float(duration) / 60; #convert to minutes

    print "duration: " + str(duration)

    mean_speed = activity['mean_speed']
    distance = activity['distance']
    distance = distance * 0.621 #convert to miles

    #enforce minimums
    if duration < MIN_DURATION or distance < MIN_DISTANCE:
        print "Error too short"
        return None
    #weed out unreasonable maximums
    if duration > MAX_DURATION or distance > MAX_DURATION:
        print "Error too long"
        return None

    return (duration, mean_speed, distance)


######my shit


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
        # for a in all_data:
        #     outfile.write((a + u'\n').encode('unicode-escape'))

    return

def addToListsFromFile(file_name):

    with open(file_name) as data_file:
        data = yaml.load(data_file)

    for activity in data['activities']:
        if activity['mode'] != 'outdoor' and activity['mode'] != 'treadmill':  # ignore exercise that isn't running
            continue

        stats = pullStatsFromRun(activity)
        if (stats):
            (duration, mean_speed, distance) = stats
            mean_speed_list.append(mean_speed)
            duration_list.append(duration)
            distance_list.append(distance)

saveDataToFile('data.txt', 4)
addToListsFromFile('data.txt')
