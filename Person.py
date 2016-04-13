#from main import pullStatsFromRun
import datetime
from Run import *

class PersonClass:
    ID = ''
    weeks = {} # { weekHash : [ run ] } #TODO: update this to reflect multiple weeks
    #currentWeek = 0 #should be unnecessary with the new weekHash implementation
    goal = None
    currentWeek = 0 #holds the current (or highest number) week

    def __init__(self, id_in, goal):
        self.ID = id_in
        self.goal = goal

    #TODO: this may or may not atually return the proper values
    def getWeekHashForDate(self, date):
        #hash each date to the most recent Sunday (since weeks start on Sundays)
        dayOfWeek = date.weekday()
        dateRet = date - datetime.timedelta(6 - dayOfWeek)

        hashStr = str(dateRet.year)
        s = str(dateRet.month)
        if len(s) == 1:
            s = '0' + s
        hashStr += s
        d = str(dateRet.day)
        if len(d) == 1:
            d = '0' + d
        hashStr += d


        return int(hashStr)
    '''
    def getWeekOfRun(self, run):
        date = run.date
        weekHash = getWeekHashForDate(date)

        try:
            weeks[weekHash].append(run)
        except:

        if weekNum == currentWeek: #in current week, don't need to do anything special
            weeks[weekNum].append(run)
        else: #new or old week, so have to first find what week it is
            weekNum = datetime.date(year, month, day).weekday()

        return 
    '''
    #run: Run object
    def addRun(self, run):
        week = self.getWeekHashForDate(run.date)
        if week > self.currentWeek:
            self. currentWeek = week
        try:
            self.weeks[week].append(run)
        except:
            self.weeks[week] = [run]

    '''
    #unnecessary because of week hash
    def newWeek(self, date):
        self.currentWeek = self.currentWeek + 1
        currentWeekDate = date
        self.weeks[self.currentWeek] = []
    '''

    def getRunsAtWeek(self, week):
        return self.weeks[week]

    def getCurrentWeekRuns(self):
        try:
            return self.weeks[self.currentWeek]
        except:
            return None

    #currentRuns: [ Run ]
    def averagesHelper(self, currentRuns):
        duration_list = []
        mean_speed_list = []
        distance_list = []

        for run in currentRuns:
            #thisRun = pullStatsFromRun(run)
            duration_list.append(run.duration)
            mean_speed_list.append(run.mean_speed)
            distance_list.append(run.distance)

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
        return week[len(week) - 1]

    #needed to be a value in a dictionary
    def __hash__(self):
        return hash((self.ID))

    def __eq__(self, other):
        return (self.ID) == (other.ID)

    def __ne__(self, other):
        # Not strictly necessary, but to avoid having both x==y and x!=y
        # True at the same time
        return not(self == other)

