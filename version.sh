#########################################################################################
#Author :@Abhishek Ranjan                                                              ##
#Email: abhishek.ranjan@oronetworks.com                                                ##                                  #Description: Script to  list all the services and Version(PROD & ENG)            ##                                  #Date: 17 July 2018                                                               ##
#########################################################################################


#!/bin/bash
#Deleting/Cleaning the directory

cd /home/scripts/FINAL

rm -rf Prod_version.txt
rm -rf Prod_service.txt
rm -f Print_service.txt
rm -f Eng_version.txt
rm -f Eng_service.txt
rm -f Eng.txt Eng_sort.txt
rm -f report.txt
rm -f report.html
rm -f sort_service.txt

# Ssh into PROD instances and executing the commands for listing version under current directory

for server in  `cat Prod_server.lst`
do
   #echo     " ********************$server Prod start*********************************"
       ssh -TAtt ubuntu@18.221.144.194 ssh -A -o ConnectTimeout=5 -o BatchMode=yes -o StrictHostKeyChecking=no ubuntu@$server "ls -ld /lunera/code/*/current | awk '{print $11}'|rev|cut -d - -f 1|rev ">> Prod_version.txt
                     sed -i 's/> //' Prod_version.txt
                     sed -i 's/\///' Prod_version.txt
# Ssh into same instances to list out services name

       ssh -TAtt ubuntu@18.221.144.194 ssh -A -o ConnectTimeout=5 -o BatchMode=yes -o StrictHostKeyChecking=no ubuntu@$server "ls -ld /lunera/code/*/current | awk '{print $9}'|cut -d / -f 4 " >>Prod_service.txt
done

# Printing the services and version in column

pr -m -t -f Prod_service.txt Prod_version.txt|column -t >> Print_service.txt
sed -i -e 's/\r//g' Print_service.txt
# Sorting the file in alphabatically

sort Print_service.txt|uniq|tee sort_service.txt


#SSH to the ENG instances and executing the commands

for server in  `cat Eng_server.lst`
do
   #echo     " ********************$server Eng start*********************************"
       ssh -i /home/scripts/LuneraDev.pem -o ConnectTimeout=5 -o BatchMode=yes -o StrictHostKeyChecking=no ubuntu@$server "ls -ld /lunera/code/*/current | awk '{print $11}' |rev|cut -d - -f 1|rev" >> Eng_version.txt
                       sed -i 's/> //' Eng_version.txt
                       sed -i 's/\///' Eng_version.txt
       ssh -i /home/scripts/LuneraDev.pem -o ConnectTimeout=5 -o BatchMode=yes -o StrictHostKeyChecking=no ubuntu@$server "ls -ld /lunera/code/*/current | awk '{print $9 }'|cut -d / -f 4 ">> Eng_service.txt
done
pr -m -t -f Eng_service.txt Eng_version.txt >> Eng.txt
# sort the files
sort Eng.txt|uniq|tee Eng_sort.txt
# Version of DASHBOARD
dash_eng=$(curl https://eng.lunera.com/version.txt)
dash_prod=$(curl https://cloud.lunera.com/version.txt)
#Print the files in column

#Print the version number of CLOUD and ENG
eng_firmware=$(
eng_firmware=$(python firmwareversion.py 'https://api.eng.lunera.com' 'ENG_DevOps' 'Orofii@-1@39'|tail -1)
prod_firmware=$(python firmwareversion.py 'https://api.cloud.lunera.com' 'Oro_prod' 'Orofii@-1@39'|tail -1)
awk 'NR==FNR{a[$1]=$2;next} ($1) in a{print $0, a[$1]}' Eng_sort.txt sort_service.txt  >> report.txt
sed  -i '1i\           VERSION-LIST-COMPARISON \nSERVICE-VERSION PROD ENG ' report.txt
sed  -i "11i\Dashboard $dash_prod$dash_eng" report.txt
sed  -i  "10i\FirmWare $prod_firmware Coming-Soon" report.txt
# Include html format
awk 'BEGIN { print "<table border=1>"}; { printf( "<tr><td>%s</td><td>%s</td><td>%s</td></tr>\n", $1, $2, $3 ) } END { print  "</table>" }' report.txt  > report.html
# send the mail
python mailsend_html.py
ubuntu@ip-172-16-1-52:/home/scripts/FINAL$
