import requests
import os
import json
import datetime
import ast

#Google Distance Matrix API key: AIzaSyCib4RJYMASjkuobKzN1OLlEiK-5E-W_6g

# boilerplate for AWS

class FlightDict(object):
    def __init__(self,data):
        self.dict = ast.literal_eval(data)



def getFlight(flightNumber, date):
    ''' Return JSON of flight with flightNumber <flightNumber> in a given UTC datetime range.
        flightNumber and date are required fields. '''

    if not flightNumber or not date:
        print("Error: 'flightNumber' and 'date' are required fields")
        raise

    r = requests.get("https://tamuhack-2018.herokuapp.com/flight?flightNumber=" + flightNumber + "&date=" + date)

    if r.status_code != 200:
        print("API returned status code " + r.status_code)
        raise

    return r.text

def getFlights(origin, destination, date):
    ''' Return JSON of all flights from 'origin' to 'destination' in a given UTC datetime range.
        'date' is a required field. '''

    if not date:
        print("Error: 'date' is a required field")
        raise

    r = requests.get("https://tamuhack-2018.herokuapp.com/flights?origin=" + origin +
    "&destination=" + destination + "&date=" + date)
    return r.json

def main():
    g = getFlight("1708", "2018-03-01T18:00-08:00")


    #a = dict(g.text.json)
    #print(type(a))
    #json_dict = json.load(g)
    #print(json_dict.dict)
    #for x in json_dict:
    #    print(x)


main()
