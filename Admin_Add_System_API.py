## Author: Jacob Chesley
##
## Admin API to add systems to the database.
## Access should not be given to users.
## Last Updated: 1/30/19

import json
import sys
import pymysql
import rds_config

# RDS settings
rds_host  = rds_config.db_rds_host
name = rds_config.db_username
password = rds_config.db_password
db_name = rds_config.db_name

def lambda_handler(event, context):
    # Return value
    ret = {'statusCode': -1, 'body': -1}
    try:
        conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
        with conn.cursor() as cur:
            cur.execute("INSERT INTO System (Sys_ID, User_ID) VALUES(%s, %s);", (event.get("sys_id"), 1))
            conn.commit()
        ret['statusCode'] = 200
        ret['body'] = "Successfully added system"
    except:
        e = sys.exc_info()[1][0]
        if e == 1045:
            ret['statusCode'] = 401
            ret['body'] = "Access denied to database"
        elif e == 1049:
            ret['statusCode'] = 403
            ret['body'] = "Database does not exist"
        elif e == 1062:
            ret['statusCode'] = 403
            ret['body'] = "System has already been added to database"
        else:
            ret['statusCode'] = 404
            ret['body'] = "Unknown error while attempting to add system to database"
        
    return {
        'statusCode': ret.get('statusCode'),
        'body': json.dumps(ret.get('body'))
    }
