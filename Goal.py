class Goal:
    completedValue = 0
    tier = None
    params = {
        #goal specifics - set these to other than None if they're relevant
        'numRuns' : None,
        'totalDuration' : None,
        'totalAvgSpeed' : None,
        'totalDistance' : None,
        #hold list of specific durations
        'runDuration' : None,
        'runAvgSpeed' : None,
        'runDistance' : None,
        'runMaxSpeed' : None,
        'runMinSpeed' : None,
        #booleans to hold whether a progression is necessary for the run-specific 
        'runDurationBool' : None,
        'runAvgSpeedBool' : None,
        'runDistanceBool' : None,
        'runMaxSpeedBool' : None,
        'runMinSpeedBool' : None
        }

    def __init__(self, tier):
        self.completedValue = 30 #fix
        self.tier = tier

    def getCompletedValue(self):
        return self.completedValue

    def checkCompletion(self):
        
        return True




'''
sample goals:
    -run three times
    -average x speed over all runs
    -run x distance in one run
    -run x distance over the week


number of runs
per run:
    duration
    average speed
    distance
    max speed
    min speed
total
    duration
    average speed
    distance


'''