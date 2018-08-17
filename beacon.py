###########################################################################################
#Author :@Abhishek Ranjan                                                               ###
#Email: abhishek.ranjan@oronetworks.com                                                 ###  
#Description : Display iBeacons status,details and configuration                        ###
#Date: 16 August 2018                                                                   ### 
###########################################################################################

#import all the modules which is required for python to run 
import sys
from pprint import pprint
import Queue
import threading
import smtplib, datetime, random
from datetime import datetime
from pytz import timezone
import pytz
import socket
import cStringIO
import json
import time
import urllib
import os
import requests
import copy

import json
from urlparse import urlparse

# Define class which declares Global Variables

class apitestclass:
    index = 0
    function = ' '
    description = ' '
    payload = {}
    headers = {}
    url = ' '
    method = 0
    status_code = ' '
    expectedcode = 0
    key = 'none'
    jsondata = {}
    validreturndata = 'pass'
    datatype = ''
    testresult = 0
    errortest = False
    executed = False
    fixture = {}

#Define class to declare local variables

class custdata:

    facilities = {} 
    floors = {} 
    suites = {}
    lamps = {}
    zones = {}
    fixtures = {}
    ibeacons = {}
#Declare APIs request

methods = ['get', 'put', 'post']

GET = 0
PUT = 1
POST = 2

#Initialise STATUS CODE

codeok = 200
badrequest = 400
notauthorized = 401
methodnotfound = 404
methodnotallowed = 405
statusnotok = 9999

testsuccess = 21
testfail = 21

#Declare main function Which will count the number of arguements passed in the script

def main():



    print len(sys.argv)
    if len(sys.argv) < 4:
       print("Usage lamps.py <api url> <username> <password>")
       exit(0)
#Formatting the order in which arguemnets should be passed
    api = sys.argv[1]
    username = sys.argv[2]
    password = sys.argv[3]

    # create customer data object 
    cusdata = custdata()

    token = login(api, username, password)

    if token == None:
        print "api error exiting ... "
        return

#Calling API token

    cusdata = getcustomerdata(api, token)

# Loop to get the building address of the username passed in the arguments

def getcustomerdata(api, token):

    mydata = custdata()
    getiBeaconState(api, token)
    getiBeaconConfiguration(api, token)    
    mydata.facilities = getfacilitiesdetails(api, token)
#Loop to get the floor details of the building address fetched by cusdata.facilities object

    #print("facilities = {0}".format(mydata.facilities))
    
    for facility in mydata.facilities:
        #print("facility = {0}".format(facility))

        mydata.floors[facility['id']] = getfloorsdetails(api, token, facility['id'])
#Loop to get the suites details of the floor fetched by cusdata.floors object

        for floor in mydata.floors[facility['id']]:
            #print("floor = {0}".format(floor))
            #print("fixtures id = {0}".format(fixtures['id']))
#This loop will get the floor id to call ibeacons id 

            mydata.suites[floor['id']] =  getsuitesdetails(api, token, floor['id'])
            mydata.ibeacons[floor['id']] = getibeaconsdetails(api, token, floor['id'])
            print("**************************Beacon Config Fixtures for Floor**********************")
            for beacon in mydata.ibeacons[floor['id']]:
                #print("fixture id = {0}".format(fixture['id']))
                print("\nfixture id = {0}".format(beacon))

        return mydata

#Define function to initialise the metadata of all APIs used 

def getfacilities(api, token):

    apitest = apitestclass()
    apitest.description = 'get facilities'
    apitest.function = 'get facilities'
    apitest.url = api + '/v1/facilities'
    apitest.headers = {'authorization': 'Bearer ' + token, 'content-type': 'application/json'}
    apitest.method = 'get'

    return runapi(apitest)['facilities']

#Define function to call Api for building address

def getfacilitiesdetails(api, token):

    apitest = apitestclass()
    apitest.description = 'get facilities inline'
    apitest.function = 'get facilities inline'
    apitest.url = api + '/v1/facilities?inline=facility'
    apitest.headers = {'authorization': 'Bearer ' + token, 'content-type': 'application/json'}
    apitest.method = 'get'

    return runapi(apitest)['facilities']

#Define function to call APIs for floors

def getfloors(api, token, facility):

    apitest = apitestclass()
    apitest.description = 'get floors'
    apitest.url = api + '/v1/' + facility + '/floors'
    apitest.headers = {'authorization': 'Bearer ' + token, 'content-type': 'application/json'}
    apitest.method = 'get'
    apitest.expectedcode = 200

    return runapi(apitest)['floors']


def getfloorsdetails(api, token, facility):

    apitest = apitestclass()
    apitest.description = 'get floors'
    apitest.url = api + '/v1/' + facility + '/floors?inline=floor'
    apitest.headers = {'authorization': 'Bearer ' + token, 'content-type': 'application/json'}
    apitest.method = 'get'
    apitest.expectedcode = 200

    return runapi(apitest)['floors']

#Define function to call APIs for beacons config fixtures for floors

def getibeaconsdetails(api, token, floor):

    apitest = apitestclass()
    apitest.description = 'get ibeacons'
    apitest.url = api + '/v1/ibeacon/' + floor + '/fixtures'
    apitest.url = apitest.url.replace('facility/', '')
    apitest.headers = {'authorization': 'Bearer ' + token, 'content-type': 'application/json'}
    apitest.method = 'get'
    apitest.expectedcode = 200
    
    return  runapi(apitest)['fixtures']

#Define function to call APIs to get beacon state 

def getiBeaconState(api, token):

    url = api + '/v1/ibeacon/state'
    headers = {'authorization' : 'Bearer ' + token,  'content-type': 'application/json' }

    data = requests.get(url,  headers=headers)
    if data.status_code == requests.codes.ok:
        binary = data.content
        Beacons_State = json.loads(binary)
        print("********************Beacons State***************************")
        print json.dumps(Beacons_State, sort_keys=True, indent=4, separators=(',', ': '))
        #print data_json

#Define function to call APIS to get beacon configuration

def getiBeaconConfiguration(api, token):

    url = api + '/v1/ibeacon/config'
    headers = {'authorization' : 'Bearer ' + token , 'content-type': 'application/json' }
   
    data = requests.get(url, headers=headers)
    if data.status_code == requests.codes.ok:
        binary = data.content
        Beacons_Config = json.loads(binary)
        print("**********************iBeacons Configuration*****************")
        print json.dumps(Beacons_Config, sort_keys=True, indent=4, separators=(',', ': '))
        #print data_json
        
    else:
        print ("{0} failed with code {1}".format(url, data.status_code))
#********These below functions are defined to call APIs for suites ,zones ,suites for future use . This function will not affect as we are not printing the result **********

def getsuites(api, token, floor):

    apitest = apitestclass()
    apitest.description = 'get suites'
    apitest.url = api + '/v1/' + floor + '/suites'
    apitest.headers = {'authorization': 'Bearer ' + token, 'content-type': 'application/json'}
    apitest.method = 'get'
    apitest.expectedcode = 200

    return  runapi(apitest)['suites']


def getsuitesdetails(api, token, floor):

    apitest = apitestclass()
    apitest.description = 'get suites'
    apitest.url = api + '/v1/' + floor + '/suites?inline=suite'
    apitest.headers = {'authorization': 'Bearer ' + token, 'content-type': 'application/json'}
    apitest.method = 'get'

    return  runapi(apitest)['suites']

def getzones(api, token, suite):

    apitest = apitestclass()
    apitest.description = 'get zones'
    apitest.url = api + '/v1/lightcontrol/' + suite + '/zones'
    apitest.url = apitest.url.replace('facility/', '')
    apitest.headers = {'authorization': 'Bearer ' + token, 'content-type': 'application/json'}
    apitest.method = 'get'
    apitest.expectedcode = 200

    return runapi(apitest)['zones']

def getzonesdetails(api, token, suite):

    apitest = apitestclass()
    apitest.description = 'get zones'
    apitest.url = api + '/v1/lightcontrol/' + suite + '/zones?inline=zone'
    apitest.url = apitest.url.replace('facility/', '')
    apitest.headers = {'authorization': 'Bearer ' + token, 'content-type': 'application/json'}
    apitest.method = 'get'

    return runapi(apitest)['zones']

def getfixturesdetails(api, token, suite):

    apitest = apitestclass()
    apitest.description = 'get fixtures'
    apitest.url = api + '/v1/' + suite + '/fixtures?inline=fixture'
    apitest.headers = {'authorization': 'Bearer ' + token, 'content-type': 'application/json'}
    apitest.method = 'get'
    apitest.expectedcode = 200
	
    return runapi(apitest)['fixtures']

def getlampsdetails(api, token, suite):

    apitest = apitestclass()
    apitest.description = 'get lamps'
    apitest.url = api + '/v1/' + suite + '/lamps?inline=lamp'
    apitest.headers = {'authorization': 'Bearer ' + token, 'content-type': 'application/json'}
    apitest.method = 'get'
    apitest.expectedcode = 200
	
    return runapi(apitest)['lamps']

#Define function for APIs methods request

def runapi(apitest):

 #       print('running api url = {0}'.format(apitest.url))

        apitest.jsondata = ' '
        apitest.roundtrip = 0
        apitest.status_code = 0

        if apitest.method == 'get':
            #print("HEADER = {0}".format(apitest.headers))
            data = requests.get(apitest.url, headers=apitest.headers)

        if apitest.method == 'put':
            data = requests.put(apitest.url, data=json.dumps(apitest.payload), headers=apitest.headers)

        if apitest.method == 'post':
            data = requests.get(apitest.url, headers=apitest.headers)

        apitest.roundtrip = data.elapsed.total_seconds()
        apitest.status_code = data.status_code
        #print(apitest.url)
        #print(data.content)
        if data.status_code == requests.codes.ok:
            try:
                apitest.jsondata = json.loads(data.content)
                return apitest.jsondata
            except Exception, e:
                print('data.content error')
                return None

#Define login function for the customer

def login(api, username, password):
    url = api + '/v1/login'

    payload = {"username": username, "password": password}
    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}

    data = requests.post(url, data=json.dumps(payload), headers=headers)

    if data.status_code == requests.codes.ok:
        print 'Hello Mr.'+ username + ' ! Your Details are as follows '
        binary = data.content
        Parsed_data = json.loads(binary)
        return Parsed_data['token']
    else:
        print 'Hello !! Your login Credential is INCORRECT'
        return None

main()
