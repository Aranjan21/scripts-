import sys
import json
import time
import urllib
import smtplib
import socket
from datetime import datetime
from pytz import timezone
import pytz
import os
import requests

server={}
diff={}

class serverstatusclass:
        servername = ''
        index = ''
        service = ''
        veng = 'X.X.XX'
        vcloud = 'X.X.XX'

def diffschema(expected, actual):
    """
    Helper function. Returns a string containing the unified diff of two multiline strings.
    """

    import difflib
    expected=expected.splitlines(1)
    actual=actual.splitlines(1)

    diff=difflib.unified_diff(expected, actual)

    return ''.join(diff)

def sendemail(user, pwd, recipient, subject, body):
    import smtplib

    FROM = user
    TO = recipient if isinstance(recipient, list) else [recipient]
    SUBJECT = subject
    TEXT = body
    print(body)

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(user, pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print('successfully sent the mail to {0}'.format(recipient))
    except:
        print('failed to send email')

'''
def sendemail(user, pwd, recipient, subject, cloudreport):
    import smtplib
    print(user)
    print(pwd)
    print(recipient)
    print(subject)
    print(cloudreport)
    FROM = user
    TO = recipient if isinstance(recipient, list) else [recipient]
    print('sendemail') 
    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), subject, cloudreport)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(user, pwd)
        server.sendmail(FROM, TO, cloudreport)
        server.close()
        print('successfully sent the mail to {0}'.format(recipient))
    except:
        print('failed to send email')
'''

def emailnotification(cloudreport, emailnotifyaddress, emailpassword):
   
    print('Sending notification ') 
    hostname = (socket.gethostname())
    date_format='%m/%d/%Y %H:%M:%S %Z'
    date = datetime.now(tz=pytz.utc)
    date = date.astimezone(timezone('US/Pacific'))
    timestamp = date.strftime(date_format)
    FROM = "jenkins@lunera.com"
        
    SUBJECT =  ' Cloud Processes Uptime Report \n'  
    TEXT = cloudreport 
    
    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
        """ % (FROM, ", ".join(emailnotifyaddress), SUBJECT, TEXT)
    server=smtplib.SMTP("smtp.office365.com", 587)
    server.starttls()
    server.login(FROM, emailpassword)
    server.sendmail(FROM, emailnotifyaddress, message)

def getprocessstatus(processstatus):

    for line in processstatus.splitlines():
        if 'Active:' in line:
            return line

def getcloudstatus(cloudstatusinfo):

    print('printing cloud status')

    global server 
    global diff

    cloudreport = ''

    cloudstatusinfo.sort(key=lambda x: x.service, reverse=True)

    for serverstatus in cloudstatusinfo:
        #if diff[serverstatus.service] == True:
           print("servername : {0} service : {1} eng : {2} cloud : {3} \n".format(serverstatus.servername, serverstatus.service, serverstatus.veng, serverstatus.vcloud))
           cloudreport +=  serverstatus.servername +  " : index :" + serverstatus.index + " : "+ serverstatus.service + " eng : " + serverstatus.veng + " cloud : " +  serverstatus.vcloud + "\n"
           #cloudreport += " servername : " + serverstatus.servername +  " service : " + serverstatus.service + " eng : " + serverstatus.veng + " cloud : " +  serverstatus.vcloud + "\n"
        #else:
           print('NO DIFF for service {0}'.format(serverstatus.service))

    return cloudreport 

def checkserviceversion(cloudstatusinfo, servicename):
    
    prevversion = ''
    versions = []

    for serverstatus in cloudstatusinfo:
        if serverstatus.service == servicename:
            versions.append(serverstatus.version)

    print(versions)

    for version in versions:
        if prevversion != '' and version != prevversion:
            return False
        else:
            prevversion = version

    return True

def insertintocloudstatus(cloudstatusinfo, servername, index, service, env, version):
    global server 
    global diff
    
    for serverstatus in cloudstatusinfo:

        if servername == 'eng' and serverstatus.index == index and serverstatus.service == service:
           print(servername)
           servername = serverstatus.servername

        if serverstatus.servername == servername and serverstatus.index == index and serverstatus.service == service:
            print('entry exists')
	
            if env == 'eng':
               serverstatus.veng = version
            if env == 'prod':
               serverstatus.vcloud = version
           
            if server[service] == 'X.X.XX':
            	server[service] = version
            elif server[service] != version: 
                diff[service] = True

            return True

    print('Adding new entry')

    serverstat = serverstatusclass()
    serverstat.servername = servername 
    serverstat.index = index
    serverstat.service = service
    if env == 'eng':
       serverstat.veng = version
    if env == 'cloud':
       serverstat.vcloud = version

    cloudstatusinfo.append(serverstat)

    return True

def getversioninfo(cloudstatusinfo, env, jumphost, servername, indexes, services):
    
    for index in indexes:
        for service in services:
            cmd="ssh -TAtt ubuntu@"  + jumphost + " ssh -A ubuntu@" + servername + index + ".dev.lunera.com 'cat /lunera/code/" + service + "/current/version.txt'"
            print(cmd)
            version  = os.popen(cmd).read().rstrip()
            print(" version {0}".format(version))
  
            insertintocloudstatus(cloudstatusinfo, servername, index, service, env, version)
            
    return True

def getccversioninfo(cloudstatusinfo, env):

    servername = 'control-center'
    index = '00'
    service = 'control-center'
    
    if env == 'eng':
       cmd = 'curl https://eng.lunera.com/version.txt'
    if env == 'prod':
       cmd = 'curl https://cloud.lunera.com/version.txt'

    version  = os.popen(cmd).read().rstrip()
    print(" version {0}".format(version))
  
    insertintocloudstatus(cloudstatusinfo, servername, index, service, env, version)

    return True

def getcassschema(env, jumphost):  

    cmd="ssh -TAtt ubuntu@"  + jumphost + " ssh -A ubuntu@cassandra0001.dev.lunera.com 'bash cqlschema.sh'"
    print(cmd)
    cassschema = os.popen(cmd).read().rstrip()
   
    return cassschema

def cloudcheck():

    emailnotifyaddress=['jayant.rai@oronetworks.com']
    user='no-reply@oronetworks.com'
    emailpassword = '5S2ZDjL74c'
    cloudreport ='\n\n-------------- LUNERA CLOUD PROCESS STATUS ------------------\n'
    jumphostcloud = '18.221.144.194'
    jumphosteng   = '13.59.242.61'
    cloudstatusinfo = []
   
    server['control-center'] = 'X.X.XX'
    server['AssetTracking'] = 'X.X.XX'
    server['data-mapper'] = 'X.X.XX'
    server['data-reducer'] = 'X.X.XX'
    server['data-api-server'] = 'X.X.XX'
    server['facilities-us'] = 'X.X.XX'
    server['service-now'] = 'X.X.XX'
    server['visibility-webhook'] = 'X.X.XX'
    server['asset-tracking-config-api'] = 'X.X.XX'
    server['electric-imp-enroll'] = 'X.X.XX'
    server['opsgenie'] = 'X.X.XX'
 
    diff['control-center'] = False
    diff['AssetTracking'] = False
    diff['data-mapper'] = False
    diff['data-reducer'] = False
    diff['data-api-server'] = False
    diff['facilities-us'] = False
    diff['service-now'] = False
    diff['visibility-webhook'] = False
    diff['asset-tracking-config-api'] = False
    diff['electric-imp-enroll'] = False
    diff['opsgenie'] = False

    assettrackingdiff = 0 
    dataapidiff = 1
    apidiff = 0     
    ccdiff = 0 

    if assettrackingdiff == 1:

       env = 'cloud'
       indexes = ['01', '02']
       services = ['AssetTracking']
       getversioninfo(cloudstatusinfo, env, jumphostcloud, 'assettracking', indexes , services)

       env = 'eng'
       indexes = ['01', '02']
       services = ['AssetTracking']
       getversioninfo(cloudstatusinfo, env, jumphosteng, 'eng', indexes , services)

    if dataapidiff == 1:

       env = 'cloud'
       indexes = ['01', '02', '03']
       services = ['data-mapper', 'data-reducer']
       getversioninfo(cloudstatusinfo, env, jumphostcloud, 'data-mapper', indexes , services)

       env = 'eng'
       indexes = ['01', '02']
       services = ['data-mapper', 'data-reducer']
       getversioninfo(cloudstatusinfo, env, jumphosteng, 'eng', indexes , services)

       env = 'cloud'
       indexes = ['01', '02', '03']
       services = ['data-api-server']
       getversioninfo(cloudstatusinfo, env, jumphostcloud, 'data-api', indexes , services)

       env = 'eng'
       indexes = ['01', '02']
       services = ['data-api-server']
       getversioninfo(cloudstatusinfo, env, jumphosteng, 'eng', indexes , services)

    if apidiff == 1:

       env = 'cloud'
       indexes = ['01', '02']
       #services = ['facilities-us',  'asset-tracking-config-api', 'visibility']
       services = ['facilities-us', 'service-now','visibility-webhook', 'asset-tracking-config-api', 'electric-imp-enroll', 'opsgenie']
       getversioninfo(cloudstatusinfo, env, jumphostcloud, 'api', indexes , services)

       env = 'eng'
       indexes = ['01', '02']
       services = ['facilities-us', 'service-now', 'visibility-webhook', 'asset-tracking-config-api', 'electric-imp-enroll']
       getversioninfo(cloudstatusinfo, env, jumphosteng, 'eng', indexes , services)

       env = 'eng'
       indexes = ['01', '02']
       services = ['opsgenie']
       getversioninfo(cloudstatusinfo, env, jumphosteng, 'opsgenie', indexes , services)

    if ccdiff == 1:
     
       getccversioninfo(cloudstatusinfo, 'eng')
       getccversioninfo(cloudstatusinfo, 'prod')

    cloudreport = getcloudstatus(cloudstatusinfo)

    #cassschemaeng = getcassschema('eng', jumphosteng)
 
    #print(cassschemaeng)

    #cassschemaprod = getcassschema('cloud', jumphostcloud)
 
    #print(cassschemaprod)

    #diffstring = diffschema(cassschemaeng, cassschemaprod)

    #print(diffstring)

    #sendemail(user, emailpassword, emailnotifyaddress, "ENG PROD DIFF REPORT", cloudreport)
    
cloudcheck()
