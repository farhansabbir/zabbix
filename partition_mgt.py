#!/usr/bin/python3

import datetime
import math
import time
import calendar

def getPossiblePartitions(months_ahead_from_now=1,partitions_per_month=10):
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
    for date in dates:
        unixtime = time.mktime(datetime.datetime(year=year,month=month,day=date,hour=23,minute=59,second=59).timetuple())
        ret[(time.strftime("%b%d%Y",time.gmtime(unixtime))).lower()] = unixtime
    return ret

print(getPossiblePartitions(1,10))
