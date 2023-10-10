# VaultWardenBackup
A python script to backup the important data from vaultwarden. 

This includes:
- Main database (db.sqlite3)
- Attachments folder

## Features
### Logging
Every step of the backup is logged to a backup.log file.

This includes info and error messages.

### Database backup
The database is backed up via the command

```
sqlite3 db.sqlite3 .backup [output_file]
```

in order to avoid corruption.

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

This script is meant to be called with via a crontab.

In Linux:
```
crontab -e
```

Add a simple command to the bottom, such as:
```
33 03 * * * python3 ~/bin/vault_warden_backup.py
```

Given that this script is located in ~/bin.
