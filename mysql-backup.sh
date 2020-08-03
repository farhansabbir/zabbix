#!/bin/bash -x
LOGFILE=/monitoring-db/mysql-server/backup.log
echo "Zabbix database structure backup started at `date`" >> $LOGFILE
TABLES=""
for filename in `find /monitoring-db/data/zabbix/ -type f -name "*ibd" ! -name "*\#P\#*" -size -1200M -printf "%p "`; do filename=${filename%%'.ibd'}; TABLES="$TABLES ${filename#'/monitoring-db/data/zabbix/'}"; done;
/monitoring-db/mysql-server/bin/mysqldump --dump-date -a -R -d -S /monitoring-db/mysql-server/mysql.sock zabbix > /mnt/$HOSTNAME/zabbix_db_struct-`date +%d%m%Y%H%M%S`
/monitoring-db/mysql-server/bin/mysqldump --dump-date -a -R -S /monitoring-db/mysql-server/mysql.sock zabbix $TABLES > /mnt/$HOSTNAME/zabbix_config_dump-`date +%d%m%Y%H%M%S`

echo "Zabbix database full backup started at `date`" >> $LOGFILE
rsync --recursive --links --acls --owner --group --progress --human-readable --compress --times --perms --update /monitoring-db/data/* "/mnt/$HOSTNAME/data/"
if [ $? -eq 0 ]
then
        echo "Zabbix database backup completed successfully at `date`" >> $LOGFILE;
else
        echo "Zabbix database backup has errors at `date`" >> $LOGFILE;
fi
ls -l /mnt/$HOSTNAME/ >> $LOGFILE;
echo "********************END OF ZABBIX BACKUP***************************" >> $LOGFILE
