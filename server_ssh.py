import os
import pexpect
import sys
from sys import argv

def conf_du(username,server_name,password,id):
    prompt='\$ $'
    #log_fptr = open("server.log", 'wb')
    service_name = 'duapp-%s-****-*******'%(gnbid)
    print ("Hello World:" ,service_name)
    child = pexpect.spawn('ssh -o StrictHostKeyChecking=no %s@%s'%(username,DU_name),timeout=10)
    child.expect("%s@%s's password:"%(username,DU_name))
    child.sendline(password)
    child.expect(prompt)
    child.sendline('login Ranjan')
    child.expect('assword:')
    child.sendline('Ranjan@123\n')
    child.expect(prompt)
    child.sendline()
    child.expect(prompt)
    child.sendline('kubectl get pods |grep <pod name>)
    child.expect(prompt)
    x = child.before.decode('ascii')
    x = x.split('\n')
    if x[1].find(service_name) != -1:
        child.sendline("kubectl exec -it %s -n t002-u000005 -- bash -c '/opt/ani/bin/confd_cli -A $ANI_CONFD_SERVICE_IPADDRESS -P $ANI_CONFD_SERVICE_PORT -u root'"%(service_name))
        child.expect('%s@%s> '%('root',service_name))
        child.sendline('configure')
        child.expect('%')
        child.sendline('some commands *)
        child.expect(":")
        child.sendline('1')
        child.expect(":")
        child.sendline('%s'%(int(id)))
        child.expect(":")
        child.sendline('22')
        child.expect(": ")
        child.sendline('1')
        child.expect(':')
        child.sendline('1')
        child.expect('%')
        child.sendline('commit')
        child.expect('%')
        child.sendline('show')
        print('\n','Sucessfully configured','\n')
    else:
        print("pod is absent")

if __name__ == "__main__":
    conf_du(str(sys.argv[1]),str(sys.argv[2]),str(sys.argv[3]),str(sys.argv[4]))
