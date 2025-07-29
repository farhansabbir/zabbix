
import calendar
from datetime import datetime
from collections import deque

YEAR = 2021     # YYYY format; e.g. 2020
START_MONTH = 11 # Jan = 1, Feb = 2 ... Dec = 12
END_MONTH = 12   # Jan = 1, Feb = 2 ... Dec = 12
FIRST_TIME_PARTITION = False


PARTITION_RANGES = list()
TABLE_NAMES = ["history", "history_uint","history_log","history_str","history_text"]
LOCATIONS = deque(["/data01/data","/data02/data","/data03/data","/data04/data","/data05/data",])
QUERIES = list()

for month in range(START_MONTH, END_MONTH+1):
    last_day_of_month = calendar.monthrange(YEAR,month)[1]
    for day in range(6,last_day_of_month + 1,6):
        DT = datetime.fromisoformat(str(YEAR)+"-" + str(month).zfill(2) + "-" + str(day + last_day_of_month%6).zfill(2) + " 23:59:59")
        partition_name = (DT.date().strftime("%b%Y").lower()) + "_" + str(day + last_day_of_month%6).zfill(2)
        PARTITION_RANGES.append({partition_name:str(DT)})

if not FIRST_TIME_PARTITION:
    for table in TABLE_NAMES:
        index = 0
        query = "alter table " + table + " add partition ("
        for partition in PARTITION_RANGES:
            key = list(partition)[0]
            #query += "partition " + str(key) + " values less than unix_timestamp(\"" + partition[key] + "\") data directory = '" + LOCATIONS[index%len(LOCATIONS)] + "' index directory = '" + LOCATIONS[index%len(LOCATIONS)] + "',"
            query += "partition " + str(key) + " values less than (unix_timestamp(\"" + partition[key] + "\")) data directory = '" + LOCATIONS[index%len(LOCATIONS)] + "',"
            index += 1
        QUERIES.append(query.rstrip(",") + ");")
        LOCATIONS.rotate()
else:
    for table in TABLE_NAMES:
        index = 0
        query = "alter table " + table + " partition by range(clock) ("
        for partition in PARTITION_RANGES:
            key = list(partition)[0]
            #query += "partition " + str(key) + " values less than (unix_timestamp(\"" + partition[key] + "\")) data directory = '" + LOCATIONS[index%len(LOCATIONS)] + "' index directory = '" + LOCATIONS[index%len(LOCATIONS)] + "',"
            query += "partition " + str(key) + " values less than (unix_timestamp(\"" + partition[key] + "\")) data directory = '" + LOCATIONS[index%len(LOCATIONS)] + "',"
            index += 1
        QUERIES.append(query.rstrip(",") + ");")
        LOCATIONS.rotate()
for query in QUERIES:
    print(query)