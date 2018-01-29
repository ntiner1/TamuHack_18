import requests
import os
import json
import datetime

from twilio.rest import Client

def lambda_handler(event, context):

    if event['session']['application']['applicationId'] != "amzn1.ask.skill.c062827e-3cc8-4ede-babd-a0add5d2dd6d":
        print ("Invalid Application ID")
        raise
    else:
        #Not using session currently
        sessionAttributes = {}

        if event['session']['new']:
            onSessionStarted(event['request']['requestId'], event['session'])
        if event['request']['type'] == "LaunchRequest":
            speechlet = onLaunch(event['request'], event['session'])
            response = buildResponse(sessionAttributes, speechlet)
        elif event['request']['type'] == "IntentRequest":
            speechlet = onIntent(event['request'], event['session'])
            response = buildResponse(sessionAttributes, speechlet)
        elif event['request']['type'] == "SessionEndedRequest":
            speechlet = onSessionEnded(event['request'], event['session'])
            response = buildResponse(sessionAttributes, speechlet)
    return (response)

def onSessionStarted(requestId, session):
    print("onSessionStarted requestId=" + requestId + ", sessionId=" + session['sessionId'])

def onSessionEnded(sessionEndedRequest, session):
    # Add cleanup logic here
    print ("Session ended")
def onLaunch(launchRequest, session):
    # Dispatch to your skill's launch.
    getWelcomeResponse()

def getWelcomeResponse():
    cardTitle = "Welcome to arrival"
    speechOutput = """Use this skill to determine when to leave for the airport."""    

def onIntent(intentRequest, session):
    intent = intentRequest['intent']
    intentName = intentRequest['intent']['name']

    if intentName == "TrackFlight":
        return getFlightInfo(intent)
    elif intentName == "AMAZON.HelpIntent":
        return getWelcomeResponse()
    elif intentName == "AMAZON.StopIntent":
        return onSessionEnded()
    else:
        print ("Invalid Intent: " + intentName)
    raise  

def getFlightInfo(intent):
    flightNumber = intent['slots']["flight_num"]['value']
    res = requests.get("https://tamuhack-2018.herokuapp.com/flight?flightNumber=" + str(flightNumber)+ "&date=2018-01-28T08:45-06:00")
    if(res.status_code==200):
        res = res.json()
        arrivalTime = res["arrivalTime"]
        airport = res["destination"]
        travelTime = getTravelTime(airport)

        leaveTime = calcLeaveTime(arrivalTime,travelTime)
        print(str(leaveTime))

        SMS("You should leave in 5 minutes to arrive at " + airport + " on time\nhttps://goo.gl/maps/PqWQF51eH3G2", "+18176821126")
        speechOutput = "AA" + str(flightNumber) + ", tracked succesfully. You will need to leave by " + str(leaveTime)
        cardTitle = speechOutput
    else:
        speechOutput = "Error connecting to API"
        cardTitle = speechOutput

    repromptText = "I didnt understand that. Please try again"
    shouldEndSession = True

    return(buildSpeechletResponse(cardTitle,speechOutput,repromptText,shouldEndSession))


def getTravelTime(airport):
    res = requests.get("https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins=2806 Carrick Ct, southlake TX 76092&destinations=" + airport + "&key=AIzaSyD-MmapiYx0aNVFB6R29twM2MJfIQ0lCVE")
    if(res.status_code == 200):
        res = res.json()
        duration = res["rows"][0]["elements"][0]["duration"]["value"]
        print("Travel Time: " + str(duration))
        return duration
    else:
        print("GOOGLE API ERROR")


def calcLeaveTime(arrivalTime, travelTime):
    ''' Calculates the time you should leave the house in order to arrive at 'arrivalTime.
        Assuming that 'travelTime' is in SECONDS.
        Assuming that arrivalTime is a STRING. '''
    
    arrivalTime = datetime.datetime.strptime(arrivalTime[:-6], "%Y-%m-%dT%H:%M")
    return (arrivalTime - datetime.timedelta(seconds=travelTime)).strftime("%I:%M %p on %A, %B %d.") #time pm, on day of week, month, day

def SMS(text,num):#,unix_time):
    print("In SMS Function")
    account_id = "AC3ceb630505e1826b12e4d9a26e73adc9"
    account_token = "0c0f8888ac6a21a8a1b02d7fc8c28fc5"
    client = Client(account_id, account_token)
    message = client.messages.create(
        to=str(num),  # "+18176821126",
        #twillio number
        from_="+19723759827",
        body=str(text)
    )
    print(message.sid)


    # --------------- Helpers that build all of the responses -----------------------
def buildSpeechletResponse(title, output, repromptText, shouldEndSession):
    return ({
        "outputSpeech": {
            "type": "PlainText",
            "text": output
        },
        "card": {
            "type": "Simple",
            "title": "Arrival - " + title,
            "content": "Arrival - " + output
        },
        "reprompt": {
            "outputSpeech": {
                "type": "PlainText",
                "text": repromptText
            }
        },
        "shouldEndSession": shouldEndSession
    })

def buildResponse(sessionAttributes, speechletResponse):
    return ({
        "version": "1.0",
        "sessionAttributes": sessionAttributes,
        "response": speechletResponse
    })
