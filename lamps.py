###########################################################################################
#Author :@Abhishek Ranjan					                                                      ###
#Email: abhishek.ranjan@oronetworks.com                                                 ###  
#Description : Display building address, floor ,suites,lamps,fixtures and zone of the cx###
#Date: 17 July 2018									                                                   ####
###########################################################################################

#Import all the modules which is required for python to run 

import sys
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

    for facility in cusdata.facilities:
        

        print("*************************BUILDING DETAILS*********************************")
        print("facility id = {0}".format(facility['id']))
        print("facility name = {0}".format(facility['name']))
        print("facility address = {0}".format(facility['address']))
        print("facility floorsInBuilding = {0}".format(facility['floorsInBuilding']))
        print("facility totalLamps = {0}".format(facility['totalLamps']))
        #raw_input()

#Loop to get the floor details of the building address fetched by cusdata.facilities object

        for floor in cusdata.floors[facility['id']]:

             print("****************************FLOOR DETAILS*******************************")
             print("floor id = {0}".format(floor['id']))
             print("floor name = {0}".format(floor['name']))
             #raw_input()

#Lop to get the suites details of the floor fetched by cusdata.floors object

             for suite in cusdata.suites[floor['id']]:

                 print("***********************SUITE DETAILS********************************")
                 print("suite id = {0}".format(suite['id']))
                 print("suite name = {0}\n".format(suite['name']))
                 print("suite wifi = {0}\n".format(suite['wifi']))
                 #raw_input()

#Loop To get the zoneID in a suites                  
                 print("****************LIST OF ALL ZONES*******************")   
                 for zone in cusdata.zones[suite['id']]:
                     print("zone id = {0}".format(zone))
                     #raw_input()

#Loop to get list of all lampsid  in a suite
    print("************LIST OF ALL LAMPS*****************")
    for lamp in cusdata.lamps[suite['id']]:
        print("lamp id = {0}".format(lamp['id']))

#Loop to get the list of all fixtures Id  in a suite
    
    print("***********LIST OF ALL FIXTURES**************")
    for fixture in cusdata.fixtures[suite['id']]:
        print("fixture id = {0}".format(fixture['id']))


#Define function to initialise the metadata of all APIs used 
def getcustomerdata(api, token):

    mydata = custdata()

    mydata.facilities = getfacilitiesdetails(api, token)

    #print("facilities = {0}".format(mydata.facilities))

    for facility in mydata.facilities:
        #print("facility = {0}".format(facility))

        mydata.floors[facility['id']] = getfloorsdetails(api, token, facility['id'])

        for floor in mydata.floors[facility['id']]:
            #print("floor = {0}".format(floor))

            mydata.suites[floor['id']] =  getsuitesdetails(api, token, floor['id'])

            for suite in mydata.suites[floor['id']]:
                #print("suite = {0}".format(suite))

                mydata.zones[suite['id']] =  getzonesdetails(api, token, suite['id'])
                mydata.lamps[suite['id']] =  getlampsdetails(api, token, suite['id'])
                mydata.fixtures[suite['id']] =  getfixturesdetails(api, token, suite['id'])
                    
    return mydata

#Define function to call Api for building address

def getfacilities(api, token):

    apitest = apitestclass()
    apitest.description = 'get facilities'
    apitest.function = 'get facilities'
    apitest.url = api + '/v1/facilities'
    apitest.headers = {'authorization': 'Bearer ' + token, 'content-type': 'application/json'}
    apitest.method = 'get'

    return runapi(apitest)['facilities']

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

#Define function to call APIs for suites

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

#Define function to call APIs for zones

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

#Define Apis to call APIs for fixtures

def getfixturesdetails(api, token, suite):

    apitest = apitestclass()
    apitest.description = 'get fixtures'
    apitest.url = api + '/v1/' + suite + '/fixtures?inline=fixture'
    apitest.headers = {'authorization': 'Bearer ' + token, 'content-type': 'application/json'}
    apitest.method = 'get'
    apitest.expectedcode = 200
	
    return runapi(apitest)['fixtures']

#Define function to call APIs for lamps

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
        print 'Hello Mr.'+ ' '+ username +  ' ! Your Details are as follows '
        binary = data.content
        Parsed_data = json.loads(binary)
        return Parsed_data['token']
    else:
        print 'Hello !! Your login Credential is INCORRECT'
        return None

main()
