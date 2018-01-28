import requests
import os
import json

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
    cardTitle = "Welcome to arrival
    speechOutput = """By using this skill it is possible to determine when to leave for the airport."""    

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
    res = requests.get("https://tamuhack-2018.herokuapp.com/flight?flightNumber=" + str(flightNumber)+ "&date=2018-03-01T08:45-06:00")
    if(res.status_code==200):
        res = res.json()
        arrivalTime = res["arrivalTime"]
        airport = res["destination"]
        duration = getTravelTime(airport)

        speechOutput = "Flight Tracked Successfully."
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





    # --------------- Helpers that build all of the responses -----------------------
def buildSpeechletResponse(title, output, repromptText, shouldEndSession):
    return ({
        "outputSpeech": {
            "type": "PlainText",
            "text": output
        },
        "card": {
            "type": "Simple",
            "title": "myTesla - " + title,
            "content": "myTesla - " + output
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
