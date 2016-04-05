from main import pullStatsFromRun

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
        currentWeek = currentWeek + 1
        weeks[currentWeek] = []

    def getRunsAtWeek(week):
        return weeks[week]

    def getCurrentWeekRuns():
        return weeks[currentWeek]

    def getCurrentWeekAverages():
        currentRuns = weeks[currentWeek]
        duration_list = []
        mean_speed_list = []
        distance_list = []

        for run in currentRuns:
            (duration, mean_speed, distance) = pullStatsFromRun(run)
            duration_list.append(duration)
            mean_speed_list.append(mean_speed)
            distance_list.append(distance)

        duration_avg = float(sum(duration_list)) / len(duration_list)
        mean_speed_avg = float(sum(mean_speed_list)) / len(mean_speed_list)
        distance_avg = float(sum(distance_list)) / len(distance_list)

        return (duration_avg, mean_speed_avg, distance_avg)