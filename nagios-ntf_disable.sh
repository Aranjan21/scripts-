#!/bin/sh
# This is a sample shell script showing how you can submit the DISABLE_HOST_NOTIFICATIONS command
# to Nagios. Adjust variables to fit your environment as necessary.

now=`date +%s`
commandfile='/usr/local/nagios/var/rw/nagios.cmd'    # uses the api which is  DISABLE_HOST_SVC_NOTIFICATIONS
logfile='/home/ubuntu/host_svc_notification.log'   # to monitor the logs 

echo $(date -u) "----------DISABLE_HOST_SVC_NOTIFICATION process is being started............."| tee -a $logfile
echo "\n"| tee -a $logfile

for hst in `cat /home/ubuntu/hostfile`   # create hostfile where you can put hostname which you want to disable 

do

/usr/bin/printf "[%lu] DISABLE_HOST_SVC_NOTIFICATIONS;$hst\n" $now > $commandfile
/usr/bin/printf "[%lu] DISABLE_HOST_NOTIFICATIONS;$hst\n" $now > $commandfile

RESULT=$?
if [ $RESULT -eq 0 ]; then
  echo $(date -u) "disable host and services notification of: $hst" | tee -a $logfile
else
  echo "\n"$(date -u) "------Script failed to run!!--------- with exit code ${RESULT}"| tee -a $logfile
  break
fi

done

res=$?
if [ $res -eq 0 ]; then
   echo "\n"$(date -u) "---------DISABLE_HOST_SVC_NOTIFICATION process is completed successfully!!---------------"| tee -a $logfile
fi
echo "\n"| tee -a $logfile
