import sys
import pprint
import Queue
import threading
import smtplib,datetime,random
from datetime import datetime
from pytz import timezone
import pytz
import socket
import cStringIO
import json, ast
import time
import urllib
import os
import requests
import copy
import uuid
import json
from urlparse import urlparse

import pymssql

username='admin'
password='wi3ALDNxVj9vPZGQ'
rdsserver='rds.dev.lunera.com'


host='rds.dev.lunera.com'
username_prod = 'admin'
password_prod = 'jaksdrey837465023grf9'
dbname='Lunera_Production'


def getschema():

        conn = pymssql.connect(rdsserver, username, password, dbname)
        cursor = conn.cursor()
        #sqlquery = 'SELECT * FROM sys.objects WHERE schema_id = SCHEMA_ID( \'dbo\')'
        sqlquery = 'SELECT NAME FROM sys.objects'
        cursor.execute(sqlquery)

        #conn.commit()
        for row in cursor:
           #sys.stdout=open("Eng-rds.sql","a")
           print(ast.literal_eval(json.dumps(row[0])))
           #print(row)
        conn.close()
       #sys.stdout.close()


def getschema_prod():

    connection = pymssql.connect(host, username_prod, password_prod, dbname)
    cursor = connection.cursor()
    query = 'SELECT * FROM sys.objects WHERE schema_id = SCHEMA_ID( \'dbo\')'
    print sqlquery
    cursor.execute(query)


    for row in cursor:
                print(row)
    connection.close()


def main():

       getschema()
main()
