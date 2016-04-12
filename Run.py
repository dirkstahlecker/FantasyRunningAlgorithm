import datetime

MIN_DURATION = 10 #minutes
MIN_DISTANCE = 0.25 #miles
MAX_DISTANCE = 200 #miles
MAX_DURATION = 20*60 #minutes

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
        print 'invalid duration: ',
        print duration
        return None
    #weed out unreasonable maximums
    if duration > MAX_DURATION or distance > MAX_DURATION:
        print 'invalid duration: ',
        print duration
        return None
    if date.year > 2020 or date.year < 1970:
        print 'invalid date: ',
        print date
        return None
    print 'returning a run'
    return Run(duration, mean_speed, distance, date)


class Run:
    duration = 0
    mean_speed = 0
    distance = 0
    date = None

    def __init__(self, duration, mean_speed, distance, date):
        print 'init'
        self.duration = duration
        self.mean_speed = mean_speed
        self.distance = distance
        self.date = date
