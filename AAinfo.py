import requests
import os
import json
import datetime


# boilerplate for AWS


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

    return r.json

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
    ##parsed = json.loads(g)
    #json.dumps(g)
main()
