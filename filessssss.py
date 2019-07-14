import datetime

now = datetime.datetime.now()
print(now.time())

from datetime import datetime


def check_orario_now(startTime, endTime):
    timeNow = "" + str(now.hour) + ":" + str(now.minute)
    nowTime = datetime.strptime(timeNow, "%H:%M")
    if startTime < endTime:
        return nowTime >= startTime and nowTime <= endTime
    else:  # Over midnight
        return nowTime >= startTime or nowTime <= endTime


timeStart = '3:00'
timeEnd = '23:00'

timeEnd = datetime.strptime(timeEnd, "%H:%M")
timeStart = datetime.strptime(timeStart, "%H:%M")
