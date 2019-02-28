## Jacob Chesley
##
## Runs specified system for specified duration (seconds)
## Records runtime in Unix Time Code to AWS RDS
## Last Updated: 2/28/19

import subprocess
import pymysql
import rds_config
import time
import sys

system = sys.argv[1]
duration = sys.argv[2]

# RDS settings
rds_host  = rds_config.db_rds_host
name = rds_config.db_username
password = rds_config.db_password
db_name = rds_config.db_name


conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
with conn.cursor() as cur:
    response = subprocess.call(["/home/pi/WayStream/run_system/system_io.sh", system, "1"])
    if response == 0: # If system successfully turned on
        cur.execute("INSERT INTO System_Runtime (Sys_ID) VALUES(%s);", (system))
        conn.commit()
        cur.execute("SELECT * FROM WayStream_Prod.System_Runtime WHERE Sys_ID = %s ORDER BY Entry_Value DESC LIMIT 1;"\
, (system))
        value = cur.fetchone()
        entry = value[0]
        start_time = value[2]
        time.sleep(float(duration))
        response = subprocess.call(["/home/pi/WayStream/run_system/system_io.sh", system, "0"])
        if response == 0:
            cur.execute("SELECT Update_StopTime(%s, %s);", (start_time, entry))
            conn.commit()
            # TODO: Implement error handling for problems with prepared function in RDS
        else:
            print("There was an error")
