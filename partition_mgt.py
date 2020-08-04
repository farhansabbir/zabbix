#!/bin/env python3

import datetime
import math
import sys
import time
import calendar

TABLES_TO_PARTITION = ["history","history_uint","history_log","history_text"]
# mountpoints where partitions will be distributed across
# idea behind is, 
#  - partitions from same table from same month should not be on same location
#  - partitions from different table for same period should not be in same location
# Example: history_uint_aug2020_10 and history_text_august2020_10 should reside on different file-systems
# Example: history_uint_aug2020_10 and history_uint_aug2020_20 must reside on different file-systems
# So number of file-systems must be equal to the maximum number of partitions
# Better to have a total of 12 file-systems and max of 10 partitions per month or
# 6 file-systems and 4 partitions per table.
# Must not be less than 6 file-systems. This is a requirement here and no debates will be encouraged.
DATA_FILESYSTEMS = ["/data01","/data02","/data03","/data04","/data05","/data06","/data10","/data11","/data12","/data07","/data08","/data09"]


def getPossiblePartitions(months_ahead_from_now=1,partitions_per_month=10):
    if (partitions_per_month * len(TABLES_TO_PARTITION))%len(DATA_FILESYSTEMS) < 2 or len(DATA_FILESYSTEMS)<6:
        print("Number of partitions must not be more than available file-systems for partitions or file-systems must be at least 6.")
        sys.exit(1)
    ret = dict()
    dates = list()
    year = datetime.datetime.today().year
    month = ((datetime.datetime.today().month + months_ahead_from_now - 1)%12)+1
    days_in_month = calendar.monthrange(year,month)[1]
    cut_off_limit = 2 # this limit governs the final date of partition, by skipping the previous date to maintain number of partitions; So don't change this
    if partitions_per_month > days_in_month/cut_off_limit:
        partitions_per_month = days_in_month
    if datetime.datetime.today().month + months_ahead_from_now > 12:
        year+=1
    for day in range((math.floor(days_in_month/partitions_per_month)), math.floor(days_in_month), (math.floor(days_in_month/partitions_per_month))):
        if (days_in_month - day) < cut_off_limit and partitions_per_month < days_in_month/cut_off_limit:
            continue
        dates.append(day)
    dates.append(days_in_month)
    for table in TABLES_TO_PARTITION:
        ret[table] = dict()
        for date in dates:
            unixtime = time.mktime(datetime.datetime(year=year,month=month,day=date,hour=23,minute=59,second=59).timetuple())
            ret[table][(time.strftime("%b%Y_%d",time.gmtime(unixtime))).lower()] = unixtime
    return ret

partitions = (getPossiblePartitions(1,10))
print(partitions)
for partition,filesystem in zip(partitions.keys(),DATA_FILESYSTEMS):
    for tables in (TABLES_TO_PARTITION):
        partition_name = (tables + "_" + partition)
        #print(partition_name + " -> " + filesystem)
