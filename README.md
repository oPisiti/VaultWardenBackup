# VaultWardenBackup
A python script to backup the important data from vaultwarden. 

This includes:
- Main database (db.sqlite3)
- Attachments folder

## Usage
```
usage: vault_warden_backup.py [-h] [-d DATA_DIR] [-b BACKUP_DIR]
                              [-m MAX_BACKUPS]

options:
  -h, --help                                 show this help message and exit
  -d DATA_DIR, --data_dir DATA_DIR
                                             Directory containing all of Vaultwarden's data
  -b BACKUP_DIR, --backup_dir BACKUP_DIR
                                             Directory to backup to
  -m MAX_BACKUPS, --max_backups MAX_BACKUPS
                                             The maximum number of backups in the backup directory.
                                             This WILL DELETE old backups
```
This script is meant to be called with via a crontab
