import datetime
from textmagic.rest import TextmagicRestClient

def calcLeaveTime(arrivalTime, travelTime):
    ''' Calculates the time you should leave the house in order to arrive at 'arrivalTime.
        Assuming that 'travelTime' is in SECONDS.
        Assuming that arrivalTime is a STRING. '''
    
    arrivalTime = datetime.datetime.strptime(arrivalTime[:-6], "%Y-%m-%dT%H:%M")
    return arrivalTime - datetime.timedelta(seconds=travelTime)

def SMS(text,num,unix_time):
    username = "ishanvasandani"
    token = "XBArTWfwovCDJj854bADTFYzIWOfXx"
    client = TextmagicRestClient(username, token)
    
    message = client.messages.create(phones=str(num), text=str(text), sendingTime=str(unix_time))

#SMS("Test 2","19036352069","151711800")
