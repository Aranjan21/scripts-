"""Streamdata.io demo."""
from pprint import pprint
import sys
import collections
import json
import time
import random

import jsonpatch
import requests
import sseclient

import argparse
import getpass

from terminaltables import AsciiTable

def print_table(data):
    """Print data as a table."""
    table_data = []
    for item in data:
        item = collections.OrderedDict(
            sorted(item.items(), key=lambda t: t[0]))
        if len(table_data) == 0:
            table_data.append(item.keys())
        table_data.append(item.values())
    table = AsciiTable(table_data)
    print(table.table)


def login(api, username, password):
    url = api + '/v1/login'
    payload = {"username": username, "password": password}
    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}

    data = requests.post(url, data=json.dumps(payload), headers=headers)

    if data.status_code == requests.codes.ok:
        binary = data.content
        Parsed_data = json.loads(binary.decode('utf-8'))
        return Parsed_data['token']
    else:
        print ('Hello !! Your login Credential is INCORRECT')
        return None

def run(data, retryCount):
    """Launch client."""
    """with requests.get(URL, stream=True) as response:"""

    parser = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-u', '--username', help='Specify username in double quotes',required=True)
    parser.add_argument('-p', '--password', help='Specify password in double quotes',required=True)
    parser.add_argument('-l', '--url', help='Specify url in double quotes',required=True)
    parser.add_argument('-t', '--sdtoken', help='Specify SDTOKEN in double quotes', default = 'MGI3NTQ0N2EtOTBmMS00MmQ0LTg3Y2UtNzM5NDU4YThhYTRj')
    args = parser.parse_args()


    print("Using the following Information for Notificataion")
    print("###################################################################################")

    api = args.url
    username = args.username
    print("USERNAME :" + username)
    password = args.password
    print("PASSWORD:" + password)
     
    sd_input_token = args.sdtoken

    token = login(api, username, password)

    if token == None:
        print ("api error exiting ... ")
        return

    DEMO_API = api + '/v1/assettracking/assetsInline'
    print("Lunera API URL for Asset Tracking Notification :" + DEMO_API)
    URL = (
    "https://streamdata.motwin.net/{}?X-Sd-Token={}".format(DEMO_API, sd_input_token)
    )
    print("StreamData URL: " + URL)
    
    print("###################################################################################")
   
    headers = {'authorization': 'Bearer ' + token }

    try:
            with requests.get(URL, stream=True, headers=headers) as response:
                client = sseclient.SSEClient(response)
                for event in client.events():
                    if event.event == "data":
                        print("Data event received")
                        last_event_id = event.id
                        data = json.loads(event.data)
                        pprint(data)

                    elif event.event == "patch":
                        print("Patch event received")
                        last_event_id = event.id
                        patch = jsonpatch.JsonPatch.from_string(event.data)
                        print("PATCH EVENT DATA:")
                        pprint(event.data)
                        patch.apply(data, in_place=True)
                        print("PATCH EVENT DATA APPLIED -> FINAL DATA:")
                        pprint(data)

                    elif event.event == "error":
                        """Print the error by default.
                           You can perform some error analysis according to
                           the message sent"""
                        print("Error: {}".format(event.data))
                        """By default, close the connnection and re-initiate a
                           new one with the Last-Event-ID of the latest message
                        """
                        client.close()

                        """Depending on the analysis of the error, you may want to
                           reconnect. That's the purpose of the code below.
                           BEWARE to perform an error analysis first. IN SOME CASE,
                           YOU DON'T WANT TO RECONNECT blindingly: bad API url,
                           authentication errors, etc. In such a case, you just
                          close the connection and deal with the error.
                           In the below example, we reconnect according to the status
                           code returned by the server.
                           NOTE that in addition, we count the number of attempts.
                           If a threshold of unsuccessful attempts has been reached,
                           we don't reconnect again: the issue is probably permanent.
                           NOTE that you can analyze the err['message'] to provide
                           a finer error message to your end users.
                           """
                        err = json.loads(event.data)
                        status = err['status']

                        """ status 2001 -> the API had an error, retry can be worthwhile
                            status 2004 -> there was a connection issue with the targeted API server, retry can be worthwhile
                            status 2008 -> there was an issue while sending the event message from the server, retry can be worthwhile
                        """
                        if retryCount < 5 and (status == 2001 or status == 2004 or status == 2008):
                            retryCount = retryCount + 1
                            """The server can set a retry in ms if not, we set a default
                                one to give to the 'Requests' lib
                                the time to close properly the connection"""
                            retry = 15
                            if event.retry is not None:
                                retry = event.retry / 1000.0

                            """If there are several parallel connections, we introduce
                               a random in order to avoid re-connnections at
                               the same time
                            """
                            time.sleep(retry + random.randint(0, 15))

                            """Re-initiate a new connection with the Last-Event-ID and
                               the latest data received (to be able to apply the next
                               patch)
                            """
                            run(data, { 'Last-Event-ID': last_event_id }, retryCount)

                    else:
                        print("Unhandled event received.")
                        client.close()
    except:
        print("Unexpected error:",  sys.exc_info()[0])

if __name__ == "__main__":
    run([],0)

