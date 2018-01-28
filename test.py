import datetime

def calcLeaveTime(arrivalTime, travelTime):
    ''' Calculates the time you should leave the house in order to arrive at 'arrivalTime'.
        Assuming that 'travelTime' is in SECONDS.
        Assuming that 'arrivalTime' is a STRING. '''
    
    arrivalTime = datetime.datetime.strptime(arrivalTime[:-6], "%Y-%m-%dT%H:%M")
    return arrivalTime - datetime.timedelta(seconds=travelTime)

def UTCtoUNIX(utc_time):
    ''' Converts STRING UTC time 'utc_time' to UNIX time (in seconds since midnight 1/1/1970).
        'utc_time' MUST BE A STRING WITH TIME ZONE INFORMATION. '''
    
    utc_time = calcLeaveTime(utc_time, 0) # convert from string to UTC
    return int((utc_time - datetime.datetime(1970, 1, 1)).total_seconds())


date = "2018-03-01T08:45-06:00"
d = calcLeaveTime(date, 0)
u = UTCtoUNIX(date)
print(str(d))
print(str(u))
