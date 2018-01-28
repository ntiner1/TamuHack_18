import requests
import os
import json
import datetime
import ast

#Google Distance Matrix API key: AIzaSyCHiE5YsOom6XH_IX2eTtM7q1kq0VeEJ2I
# boilerplate for AWS

class FlightDict(object):
    def __init__(self,data):
        self.dict = ast.literal_eval(data)

# GET /user
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
    return r.json()

# POST /user
def postUSer(firstName, lastName, email, gender, aadvantageNumber):
    ''' Creates and returns a new user with given paramaters.
        'firstName', 'lastName', 'email', and 'gender' are required fields.
        'email' must be a properly encoded email address.
        'gender' options are 'Male', 'Female', and 'Other'. '''

    if not firstName or not lastName or not email or not gender:
        print("Invalid parames entered. Request not sent to API.")
        raise
    if gender != "Male" and gender != "Female" and gender != "Other":
        print("Invalid gender entered, lol. Request not send to API.")
        raise
    r = requests.post("https://tamuhack-2018.herokuapp.com/user?firstName=" + firstName + 
        "&lastName=" + lastName + "&email=" + email + "&gender=" + gender +
        "&aadvantageNumber=" + aadvantageNumber)
    if r.status_code == 400:
        # even if not created, a JSON is still returned by the API
        print("API returned status code " + r.status_code + ". User not created.")
    return r.json()

# GET /reservation
def getReservation(recordLocator):
    ''' Return JSON of reservation with recordLocator 'recordLocator'.
        'recordLocator is a required field. '''

    if not recordLocator:
        print("Error: 'recordLocator is a required field.")
        raise
    r = requests.get("https://tamuhack-2018.herokuapp.com/reservation?recordLocator=" + recordLocator)
    if r.status_code == 500:
        # even when no reservation is found, a JSON is still returned by the API
        print("Reservation with recordLocator " + recordLocator + " not found.")
    return r.json()

# POST /reservation
def postReservation(userId, flightIds):
    ''' Creates and returns a new reservation for the user with 'userId' and an ARRAY of flight IDs
        'flightIds'.
        'userId' and 'flightIds' are required fields. '''

    if not userId or not flightIds:
        print("Error: invalid parameters entered. Request not sent.")
        raise
    if len(flightIds) < 1:
        print("Error: length of array flightIds must be at least 1.")
        raise
    
    # create the request URL with a fun loop
    request_url = "https://tamuhack-2018.herokuapp.com/reservation?userId=" + userId + "&flightIds="
    for i in range(0, flightIds.size()):
        request_url += flightIds[i]
        if i < flightIds.size() - 1:
            request_url += ","

    r = requests.post(request_url)
    if r.status_code == 400:
        # if this error message occurs, a JSON is not returned by the API
        print("API returned status code " + r.status_code + ". Reservation was not created.")
        return ""
    return r.json()

# GET /flight
def getFlight(flightNumber, date):
    ''' Return JSON of flight with flightNumber 'flightNumber' in a given UTC datetime range. 
            flightNumber and date are required fields. '''

    if not flightNumber or not date:
        print("Error: 'flightNumber' and 'date' are required fields")
        raise
    r = requests.get("https://tamuhack-2018.herokuapp.com/flight?flightNumber=" + flightNumber + "&date=" + date)
    if r.status_code != 200:
        print("API returned status code " + r.status_code)
        raise
    return r.json()

# GET /flights
def getFlights(origin, destination, date):
    ''' Return JSON of all flights from 'origin' to 'destination' in a given UTC datetime range.
        'date' is a required field. '''

    if not date:
        print("Error: 'date' is a required field")
        raise
    r = requests.get("https://tamuhack-2018.herokuapp.com/flights?origin=" + origin + "&destination=" + destination + "&date=" + date)
    if r.status_code != 200:
        print("API returned status code " + r.status_code)
        raise
    return r.json()

# POST /flightStatus
def postFlightStatus(flightNumber, status):
    ''' Updates the status of the flight with flightId 'flightNumber' using status 'status'.
        'status' options are 'On-Time', 'Delayed', and 'Cancelled'.
        Return the updated flight information. '''

    if status != "On-Time" and status != "Delayed" and status != "Cancelled":
        print("Invalid status passed to API. Request not sent.")
        raise
    r = requests.post("https://tamuhack-2018.herokuapp.com/flightStatus?flightId=" + flightNumber + "&flightStatus=" + status)
    if r.status_code == 500:
        # even if invalid, a JSON is still returned by the API
        print("Error: invalid argument passed to API.")
    return r.json()

# GET /airports
def getAirports(code):
    ''' Return JSON of airport with code 'code'. If no 'code' parameter passed, JSON of all airports
        returned. '''

    r = requests.get("https://tamuhack-2018.herokuapp.com/airports?code=" + code)
    if r.status_code != 200:
        print("API returned status code " + r.status_code)
        raise
    return r.json()

