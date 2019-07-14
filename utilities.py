from datetime import datetime
import re


def check_orario_now(startTime, endTime):
    now = datetime.now()
    timeNow = "" + str(now.hour) + ":" + str(now.minute)
    nowTime = datetime.strptime(timeNow, "%H:%M")
    if startTime < endTime:
        return nowTime >= startTime and nowTime <= endTime
    else:  # Over midnight
        return nowTime >= startTime or nowTime <= endTime


def check_coordinates(latitude, longitude):
    latitude_pattern = re.compile(r"^(\+|-)?(?:90(?:(?:\.0{1, 6})?)|(?:[0-9]|[1-8][0-9])(?:(?:\.[0-9]{1,6})?))$")
    longitude_pattern = re.compile(
        r"(\+|-)?(?:180(?:(?:\.0{1,6})?)|(?:[0-9]|[1-9][0-9]|1[0-7][0-9])(?:(?:\.[0-9]{1,6})?))$")

    lat_result = latitude_pattern.match(latitude)
    long_result = longitude_pattern.match(longitude)
    if (lat_result is not None) and (long_result is not None):
        if (len(lat_result.string) > 0) and (len(long_result.string) > 0):
            return lat_result, long_result
    else:
        return None
