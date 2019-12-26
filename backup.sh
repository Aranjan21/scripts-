#!/bin/bash
#Author :@Abhishek Ranjan
#email: chunnuabhishek21@gmail.com
#Script to prompt to backup files and location 
#The file will be search on from the user's home 
#directory and can only be backed up to a directory 
#within $HOME
#Last Edited 4th Jan
read -p "which file types do you want to backup :" file_suffix
read -p "Which directory you want to backup to :" dir_name
#The next lines creates the directory if it does not exist
test -d $HOME/$dir_name ||mkdir -m 700 $HOME/$dir_name
#The fine command will copy files the match the search criteria 
# is .sh . The -path, -prune and -O
#options are to exclude the backdirectory from the 
#backup
find $HOME -path $HOME/$dir_name -prune -o \
-name "*$file_suffix" -exec cp {} $HOME/$dir_name/ \;
exit 0
