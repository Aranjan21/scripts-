#!/usr/bin/python3
#Author: Tushar
#Version: 0.0.1
import os, smtplib, sys
import pandas as pd
from subprocess import call, run

previousfile = 'data-previous.csv'
currentfile = 'data-current.csv'
working_dir = "/home/ubuntu/usage"

ENV = os.getenv("ENV", "cloud")
FROM = "jenkins@lunera.com"
email_notify_address=["ryoung@lunera.com"]
# email_notify_address=["sgandotra@lunera.com", "ryoung@lunera.com", "jrai@lunera.com", "kho@lunera.com"]

def reportcompare():
    p = pd.read_csv(previousfile)
    c = pd.read_csv(currentfile)
    m = p.merge(c, on='Server', suffixes=('_Pre', '_Cur'))
    m = m[['Server', 'Cpu_Pre', 'Cpu_Cur', 'Memory_Pre', 'Memory_Cur', 'Disk_Pre', 'Disk_Cur', 'Db_Con_Pre', 'Db_Con_Cur', 'Msg_Pre', 'Msg_Cur']]
    m.to_csv('data.csv', sep=',', encoding='utf-8')


def csv2html_msg():
    os.chdir(working_dir)
    from fabfile import generate_stats
    generate_stats()
    reportcompare()
    try:
        os.remove('msg.html')
    except OSError:
        pass
    run(["/usr/local/bin/csv2html", "-omsg.html", "data.csv"])

def send__mail():
    SUBJECT = ENV.upper() + " Lunera Server Usage Report | Region : Ohio\nContent-Type: text/html"
    with open ("msg.html", "r") as myfile:
        TEXT = myfile.read()

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(email_notify_address), SUBJECT, TEXT)
    server=smtplib.SMTP("smtp.office365.com", 587)
    server.starttls()
    password = "Lun@2017!"
    server.login(FROM, password)
    server.sendmail(FROM, email_notify_address, message)

csv2html_msg()
send__mail()
