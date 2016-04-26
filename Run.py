import datetime

MIN_DURATION = 10 #minutes
MIN_DISTANCE = 0.25 #miles
MAX_DISTANCE = 200 #miles
MAX_DURATION = 20*60 #20 hours in minutes
MAX_YEAR = 2020
MIN_YEAR = 1970

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
        outStr += '"date": "' + str(self.date)
        outStr += '"}'
        return outStr
    
    def toJsonString(self):
        return self.toString()
    

