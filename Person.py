#from main import pullStatsFromRun

def pullStatsFromRun(activity):
    (duration, mean_speed, distance) = activity

    duration = float(duration) / 60; #convert to minutes
    distance = distance * 0.621 #convert to miles

    ''' #not necessary because of already being taken into account?
    #enforce minimums
    if duration < MIN_DURATION or distance < MIN_DISTANCE:
        return None
    #weed out unreasonable maximums
    if duration > MAX_DURATION or distance > MAX_DURATION:
        return None
    '''

    return (duration, mean_speed, distance)

class PersonClass:
    ID = ''
    weeks = {} # { week : [ run ] } #TODO: update this to reflect multiple weeks
    currentWeek = 0
    goal = None

    def __init__(self, id_in, goal):
        self.ID = id_in
        self.weeks[self.currentWeek] = []
        self.goal = goal

    def addRun(self, run):
        if len(run) != 3:
            return False
        self.weeks[self.currentWeek].append(run)
        return True

    def newWeek(self):
        self.currentWeek = self.currentWeek + 1
        self.weeks[self.currentWeek] = []

    def getRunsAtWeek(self, week):
        return self.weeks[week]

    def getCurrentWeekRuns(self):
        try:
            return self.weeks[self.currentWeek]
        except:
            return None

    def averagesHelper(self, currentRuns):
        duration_list = []
        mean_speed_list = []
        distance_list = []

        print 'currentRuns: ',
        print currentRuns

        for run in currentRuns:
            (duration, mean_speed, distance) = pullStatsFromRun(run)
            duration_list.append(duration)
            mean_speed_list.append(mean_speed)
            distance_list.append(distance)

        duration_avg = float(sum(duration_list)) / len(duration_list)
        mean_speed_avg = float(sum(mean_speed_list)) / len(mean_speed_list)
        distance_avg = float(sum(distance_list)) / len(distance_list)

        return (duration_avg, mean_speed_avg, distance_avg)

    def getCurrentWeekAverages(self):
        return self.averagesHelper(self.weeks[self.currentWeek])

    def getTotalAverages(self):
        '''
        runs = []
        for week in self.weeks:
            runs.append(week)
        '''
        return self.averagesHelper(self.weeks[self.currentWeek]) #runs

    def getMostRecentRun(self):
        week = self.weeks[self.currentWeek] #TODO: make this the most recent week
        print 'week: ',
        print week
        return week

    #needed to be a value in a dictionary
    def __hash__(self):
        return hash((self.ID))

    def __eq__(self, other):
        return (self.ID) == (other.ID)

    def __ne__(self, other):
        # Not strictly necessary, but to avoid having both x==y and x!=y
        # True at the same time
        return not(self == other)

