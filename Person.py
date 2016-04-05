class Person:
    weeks = [] #[ [ { duration , mean_speed , distance } ] ]
    currentWeek = 0

    def __init__():
        weeks[0] = []

    def addRun(run):
        if len(run) != 3:
            return False
        if type(run) != dict:
            return False
        weeks[currentWeek].append(run)
        return True

    def newWeek():
        currentWeek++
        weeks[currentWeek] = []

    def getRunsAtWeek(week):
        return weeks[week]

    def getCurrentWeekRuns():
        return weeks[currentWeek]