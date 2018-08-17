import sys
import Queue
import threading
import pycurl
import cStringIO
import json
import time
import urllib
import os
import requests

import smtplib,datetime,random
from datetime import datetime
from pytz import timezone
import pytz
import socket

import json
from urlparse import urlparse

api=sys.argv[1]
username=sys.argv[2]
password=sys.argv[3]



def main():
    global api
    token = login(api,username,password)
    getAssetTrackingStatus(api, token)
    getAllUUIDs(api, token)
    getAllAssets(api, token)

def login(api,username,password):

        url = api + '/v1/login'
        global customerId

        payload = {"username":username,"password":password}
        headers = {'Content-type': 'application/json', 'Accept': 'application/json'}

        data = requests.post(url, data=json.dumps(payload), headers=headers)

        binary = data.content
        login_data = json.loads(binary)
        print login_data
        customerId = login_data['customerId']
        print ()
        print ("CUSTOMER ID {0}".format(login_data['customerId']))
        
        return login_data['token']

def getAssetTrackingStatus(api, token):

    url = api + '/v1/assettracking/enabled'
    headers = {'authorization' : 'Bearer ' + token , 'content-type': 'application/json' }
   

    data = requests.get(url, headers=headers)
    if data.status_code == requests.codes.ok:
        binary = data.content
        Asset_status = json.loads(binary)
        print("Asset_status = {0}".format(Asset_status))
        print("id")
    else:
        print ("{0} failed with code {1}".format(url, data.status_code)) 


def getAllUUIDs(api, token):

    url = api + '/v1/assettracking/uuids'
    headers = {'authorization' : 'Bearer ' + token,  'content-type': 'application/json' }

    data = requests.get(url,  headers=headers)
    if data.status_code == requests.codes.ok:
        binary = data.content
        Asset_UUids = json.loads(binary)
        print("Asset_UUids = {0}".format(Asset_UUids))
        
    else:
        print ("{0} failed with code {1}".format(url, data.status_code))

def getAllAssetTypes(api, token):

    url = api + '/v1/assettracking/assettypes'
    headers = {'authorization': 'Bearer ' + token, 'content-type': 'application/json'}
    
    data = requests.get(url,  headers=headers)
    if data.status_code == requests.codes.ok:
        binary = data.content
        Asset_Types = json.loads(binary)
        print("Asset_Types = {0}".format(Asset_Types))
        print data_json
     
    else:
        print ("{0} failed with code {1}".format(url, data.status_code))

def getAllAssets(api, token):

    url = api + '/v1/assettracking/assets?inline=location'
    headers = {'authorization': 'Bearer ' + token, 'content-type': 'application/json'}
    
    data = requests.get(url,  headers=headers)
    if data.status_code == requests.codes.ok:
        binary = data.content
        All_Assets = json.loads(binary)
        #print("All_Assets = {0}".format(All_Assets))
        print json.dumps(All_Assets, sort_keys=True,indent=4, separators=(',', ': '))
     
    else:
        print ("{0} failed with code {1}".format(url, data.status_code))



if __name__ == "__main__":
        main()
