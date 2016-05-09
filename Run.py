import datetime

MIN_DURATION = 10 #minutes
MIN_DISTANCE = 0.25 #miles
MAX_DISTANCE = 200 #miles
MAX_DURATION = 20*60 #20 hours in minutes
MAX_YEAR = 2020
MIN_YEAR = 1970


#constants for scoring
MEAN_SPEED_DIFF_PROP_CONST = 2
DURATION_PROP_CONST = 1
DISTANCE_PROP_CONST = 1.25

def scoreRun(person, goal):
    score = 0
    score += goal.check()

    (duration_avg, mean_speed_avg, distance_avg) = person.getCurrentWeekAverages() 
    (duration_total, mean_speed_total, distance_total) = person.getTotalAverages()
    
    duration_diff = duration_avg - duration_total
    mean_speed_diff = mean_speed_avg - mean_speed_total
    distance_diff = distance_avg - distance_total
    
    score += duration_diff * MEAN_SPEED_DIFF_PROP_CONST
    score += mean_speed_diff * MEAN_SPEED_DIFF_PROP_CONST
    score += distance_diff * DISTANCE_PROP_CONST

    if score != 15:
        print score

    return score

def pullStatsFromRun(activity):
    duration = activity['duration']
    duration = float(duration) / 60; #convert to minutes

    mean_speed = activity['mean_speed']
    distance = activity['distance']
    distance = distance * 0.621 #convert to miles

    date = activity['start_time']
    #date is string, e.g. "2013-10-24T16:19:04.000Z"
    year = date[0:4]
    month = date[5:7]
    day = date[8:10]
    date = datetime.date(int(year), int(month), int(day))

    #enforce minimums
    if duration < MIN_DURATION or distance < MIN_DISTANCE:
        return None
    #weed out unreasonable maximums
    if duration > MAX_DURATION or distance > MAX_DURATION:
        return None
    if date.year < MIN_YEAR or date.year > MAX_YEAR:
        return None

    return Run(duration, mean_speed, distance, date)


class Run:
    duration = 0
    mean_speed = 0
    distance = 0
    date = None
    score = 0

    def __init__(self, duration, mean_speed, distance, date):
        self.duration = duration
        self.mean_speed = mean_speed
        self.distance = distance
        self.date = date

    def toString(self):
        outStr = '{'
        outStr += '"duration": "' + str(self.duration) + '", '
        outStr += '"mean_speed": "' + str(self.mean_speed) + '", '
        outStr += '"distance": "' + str(self.distance) + '", '
        outStr += '"date": "' + str(self.date) + '", '
        outStr += '"score": "' + str(self.score) 
        outStr += '"}'
        return outStr

    def addScore(self, score):
        self.score = score
    
    def toJsonString(self):
        return self.toString()
    

