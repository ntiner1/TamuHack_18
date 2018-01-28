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
    return r.text

def getFlights(origin, destination, date):
    ''' Return JSON of all flights from 'origin' to 'destination' in a given UTC datetime range.
        'date' is a required field. '''

    if not date:
        print("Error: 'date' is a required field")
        raise
    r = requests.get("https://tamuhack-2018.herokuapp.com/flights?origin=" + origin +
    "&destination=" + destination + "&date=" + date)
    if r.status_code != 200:
        print("API returned status code " + r.status_code)
        raise
    return r.json

def getAirports(code):
    ''' Return JSON of airport with code 'code'. If no 'code' parameter passed, JSON of all airports
        returned. '''

    r = requests.get("https://tamuhack-2018.herokuapp.com/airports?" + code)
    if r.status_code != 200:
        print("API returned status code " + r.status_code)
        raise
    return r.json

def getUser(email):
    ''' Return JSON of user with email 'email'. Returns nothing if no user with email 'email' found.
        'email' is a required field. Ensure that 'email' is encoded properly. '''

    if not email:
        print("Error: 'email' is a required field")
        raise
    r = requests.get("https://tamuhack-2018.herokuapp.com/user?email=" + email)
    if r.status_code == 400:
        # even if not found, a JSON is still returned by the API
        print("No user with email " + email + " found.")
    return r.json

def postFlightStatus(flightNumber, status):
    ''' Updates the status of the flight with flightId 'flightNumber' using status 'status'.
        status options are 'On-Time', 'Delayed', and 'Cancelled'. '''

    if status != "On-Time" or status != "Delayed" or status != "Cancelled":
        print("Invalid status passed to API. Request not sent.")
        raise
    r = requests.post("https://tamuhack-2018.herokuapp.com/flightStatus?flightId=" + flightNumber +
     "&flightStatus=" + status)
    if r.status_code == 500:
        # even if invalid, a JSON is still returned by the API
        print("Error: invalid argument passed to API.")
    return r.json


def main():
    g = getFlight("1708", "2018-03-01T18:00-08:00")
    print(g)
main()
