import subprocess
from datetime import datetime
from pathlib import Path

def main():
    now = datetime.now()

    homeDir = str(Path.home())
    dataDir = homeDir + "/docker-Vaultwarden/vw-data/"

    # Creating the backup folder
    baseBackupDir = "/Archive/Vaultwarden-backup/"
    backupDir = baseBackupDir + "backup-" + now.strftime("%Y-%m-%d@%H:%M:%S") + "/"
    subprocess.run(["mkdir", "-p", backupDir])

    # sqlite database
    databaseName = "db.sqlite3"
    databasePath = dataDir + databaseName
    subprocess.run(["sqlite3", databasePath, f".backup {backupDir}{databaseName}"])

    # Attachments directory
    attachmentsName = "attachments/"
    attachmentsDir = dataDir + attachmentsName
    subprocess.run(["cp", "-r", attachmentsDir, backupDir + attachmentsName])

    # TODO: Delete all backup directories older than a month
    subprocess.run(["find", baseBackupDir, "-type", "d", "-mtime", "+1", "-name", "'backup*'", "-delete"])

if __name__ == "__main__":
    main()