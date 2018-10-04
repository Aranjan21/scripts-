import os
import shutil

def main():
        rotate_log_file("mail3.py")
        rotate("mail3.py")

def rotate_log_file(path):
        if not os.path.exists(path):
        #the file is missing so creat it
                new_file=file(path,"w")
        #close the new file immediatiely , which leaves it empty .
                del new_file
        #now rotate it
                rotate(path)

def make_version_path(path, version):
        if version == 0:
                #No suffix for version 0,the current version returns path
                return path
        else:
                #Append a suffix to indicate the older version .
                return path + "." + str(version)

def rotate(path, version=0):
        #Consider the name of the version we are rotating .
        old_path = make_version_path(path, version)
        if not os.path.exists(old_path):
                #It doesnt exist , so complain.
                raise IOError("'%s' doesnt exist" % path)
        # Construct the new version name for this file .
        new_path = make_version_path(path, version + 1)
        #IS there an already a version with this name
        if os.path.exists(new_path):
                #Yes Rotate itout of the way first :
                rotate(path, version + 1)
        # Now we can rename the vesion safely.
        shutil.move(old_path, new_path)


main()
