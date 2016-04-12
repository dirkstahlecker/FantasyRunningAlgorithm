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

    #enforce minimums
    if duration < MIN_DURATION or distance < MIN_DISTANCE:
        return None
    #weed out unreasonable maximums
    if duration > MAX_DURATION or distance > MAX_DURATION:
        return None
    return Run(duration, mean_speed, distance, None)


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
