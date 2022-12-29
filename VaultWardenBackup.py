#!/usr/bin/python3

import subprocess
import glob
import os
import logging
import re
from datetime import datetime
from pathlib import Path


def main():

    logging.basicConfig(filename = "/Archive/Vaultwarden-backup/backup.log", format='%(levelname)s %(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)
    logging.info("----- Starting Backup -----")

    now = datetime.now()

    homeDir = str(Path.home())
    dataDir = homeDir + "/docker-Vaultwarden/vw-data/"
    baseBackupDir = "/Archive/Vaultwarden-backup/"
    backupFileInitString = "backup-"

    # Getting the newest and oldest directories in baseBackupDir: https://stackoverflow.com/questions/10983705/how-to-get-the-newest-directory-in-python/10983925
    logging.info(f"Getting newest and oldest directories in {baseBackupDir}")
    listOfDir = [f"{baseBackupDir}{d}" for d in os.listdir(f"{baseBackupDir}") if os.path.isdir(f"{baseBackupDir}{d}")]
    listOfDir = [dir for dir in listOfDir if backupFileInitString in dir]      #Getting only the backup folders (excludes .stfolder) CHANGE IN CASE OF MODIFICATION OF BACKUP FOLDERS NAMES (specially backupFileInitString)
    listOfDir.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    latestDir = listOfDir[0]
    oldestDir = listOfDir[-1]
    logging.info(f"Latest backup:   {re.findall('backup-.*', latestDir)[0]}")
    logging.info(f"Oldest backup:   {re.findall('backup-.*', oldestDir)[0]}")

    # Creating the backup folder
    backupDir = baseBackupDir + backupFileInitString + now.strftime("%Y.%m.%d-%Hh.%Mmin.%Ss") + "/"
    logging.info(f"Creating backup: {re.findall(f'{backupFileInitString}.*', backupDir)[0][:-1]}")
    subprocess.run(["mkdir", "-p", backupDir])
    logging.info("Success")

    # sqlite database
    logging.info("Backing up sqlite3 database")
    databaseName = "db.sqlite3"
    databasePath = dataDir + databaseName
    subprocess.run(["sqlite3", databasePath, f".backup {backupDir}{databaseName}"])
    logging.info("Success")

    # Attachments directory
    logging.info("Backing up attachments directory")
    attachmentsName = "attachments/"
    attachmentsDir = dataDir + attachmentsName
    subprocess.run(["cp", "-r", attachmentsDir, backupDir + attachmentsName])
    logging.info("Success")

    # Checking if the latest directory is the same as the newly created one: https://www.tecmint.com/compare-find-difference-between-two-directories-in-linux/
    diff = subprocess.run(["diff", "-qr", latestDir, backupDir], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if diff.stdout == b'':
        logging.info("New backup is the same as the latest backup. Deleting new backup")
        subprocess.run(["rm", "-r", backupDir])                       # Deleting new backup in case it is the same as latest backup
        logging.info("Success")

    # Deleting oldest backup directory in case of more than 30 backups
    if len(listOfDir) > 30:
        logging.info(f"There are more than 30 backups. Removing the oldest one: {re.findall(f'{backupFileInitString}.*', oldestDir)[0]}")
        subprocess.run(["rm", "-r", oldestDir])
        logging.info("Success")

    logging.info("")

if __name__ == "__main__":
    main()
