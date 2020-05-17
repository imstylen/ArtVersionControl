import time
import os
from shutil import copy2
import datetime

def commit_to_master(dir_path, root_path, now_time):

    items = os.listdir(dir_path)

    dir_path = dir_path + "\\"

    project_files = []
    project_folders = []

    for item in items:

        file_path = dir_path + item

        if(os.path.isfile(dir_path+item)):
            project_files.append(item)
        else:
            project_folders.append(item)


    for folder in project_folders:
        if folder != "BACKUP":

            backup_dir = root_path + "\\" + "BACKUP" +"\\" + now_time + dir_path[len(root_path):] + folder + "\\"

            if os.path.exists(backup_dir) == False:
                os.makedirs(backup_dir)

            commit_to_master(dir_path + folder,root_path, now_time)

    for file in project_files:
        if file != "Backup.py" and file != "Backup.bat":
            backup_path = root_path + "\\" + "BACKUP" + "\\" + now_time + dir_path[len(root_path):]
            src = dir_path + file

            current_revision = 0
            revision_exists = True
            mtime = 0.0
            while revision_exists:
                dst = backup_path + "Backup" + "_" + file
                if os.path.exists(dst):
                    current_revision = current_revision + 1
                    mtime = os.path.getmtime(dst)
                else:
                    revision_exists = False

                    delta = abs(mtime - os.path.getmtime(src))

                    if delta > 1.0 or current_revision == 0:

                        copy2(src,dst)
                        print(file + " has been backed up!")


    return

if __name__ == '__main__':

    print("Performing backup on all modified project files.")
    start_time = time.time()
    root_path = os.path.dirname(os.path.realpath(__file__))
    now_time = datetime.datetime.now().strftime("%m_%d_%Y %a %I-%M-%S %p")
    commit_to_master(root_path+"\\" + "Master",root_path,now_time)

    print("---- Backup completed in %.3f seconds ---" %(time.time() - start_time))
