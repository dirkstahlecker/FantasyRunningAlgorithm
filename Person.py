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

    #run: Run object
    def addRun(self, run):
        week = self.getWeekHashForDate(run.date)
        print 'week: ',
        print week
        print 'hashed from this date: ',
        print run.date
        if week > self.currentWeek:
            self. currentWeek = week
        try:
            self.weeks[week].append(run)
        except:
            self.weeks[week] = [run]

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
            if type(run) == int:
                continue #TODO: hacked fix
            duration_list.append(run.duration)
            mean_speed_list.append(run.mean_speed)
            distance_list.append(run.distance)

        duration_avg = float(sum(duration_list)) / len(duration_list)
        mean_speed_avg = float(sum(mean_speed_list)) / len(mean_speed_list)
        distance_avg = float(sum(distance_list)) / len(distance_list)

        return (duration_avg, mean_speed_avg, distance_avg)

    def getCurrentWeekAverages(self):
        runs = self.weeks[self.currentWeek]
        return self.averagesHelper(runs)

    def getTotalAverages(self):
        runs = []
        for week in self.weeks:
            for run in self.weeks[week]:
                runs.append(run)
        
        return self.averagesHelper(runs)

    def getMostRecentRun(self):
        week = self.weeks[self.currentWeek]
        return week[len(week) - 1]

    def getMostRecentWeekRuns(self):
        return self.weeks[self.currentWeek]

    def getTotalNumberOfRuns(self):
        count = 0
        for week in self.weeks:
            for run in self.weeks[week]:
                count += 1
        return count
    
    def toJsonString(self):
        outStr = '{'
        outStr += '"id": "' + self.ID + '", '
        outStr += '"goal": ' + self.goal.toJsonString() + ', '
        outStr += '"currentWeek": "' + str(self.currentWeek) + '", '
        outStr += '"weeks": ['
        for week in self.weeks:
            outStr += '{"hash": "' + str(week) + '", '
            outStr += '"runs": ['
            for run in self.weeks[week]:
                outStr += run.toJsonString() + ', '
            outStr = outStr[:len(outStr) - 2]
            outStr += ']}, '
        outStr = outStr[:len(outStr) - 2] 
        outStr += ']}'
        return outStr
    

    #needed to be a value in a dictionary
    def __hash__(self):
        return hash((self.ID))

    def __eq__(self, other):
        return (self.ID) == (other.ID)

    def __ne__(self, other):
        # Not strictly necessary, but to avoid having both x==y and x!=y
        # True at the same time
        return not(self == other)

