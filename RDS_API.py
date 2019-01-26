## Author: Jacob Chesley
##
## Initial API structure for database calls
## Last Updated: 1/25/19

import json
import sys
import pymysql
import rds_config

# RDS settings
rds_host  = rds_config.db_rds_host
name = rds_config.db_username
#password = "123"
password = rds_config.db_password
db_name = rds_config.db_name

def create_account(event, ret, conn):
    with conn.cursor() as cur:
        try:
            create = event.get("data")
            cur.execute("INSERT INTO User (First_Name, Last_Name, Email, Username, Secure_Password, User_ID) VALUES(%s, %s, %s, %s, %s, %s);", (create.get("f_name"), create.get("l_name"), create.get("email"), create.get("username"), create.get("secure_password"), create.get("user_id"),))
            conn.commit()
            ret['statusCode'] = 200
            ret['body'] = "Successfully created account"
        except:
            ret['statusCode'] = 400
            ret['body'] = "Bad Request (TODO: Implement more fine grained error codes here)"
            
def testing(event, ret, conn):
    ret['statusCode'] = 200
    ret['body'] = "Did this really work?!?!"

def lambda_handler(event, context):
    # List of functions that may be called
    switch={'create_account': create_account, 'testing': testing}
    
    # Return value
    ret = {'statusCode': -1, 'body': -1}
    no_error = 1

    try:
        conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
    except:
        ret['statusCode'] = 404
        ret['body'] = "Unable to connect with Database"
        no_error = 0
        
    if no_error:
        # Find what method needs to be executed and call method of "name"
        # E.g. 'switch[request](event, ret, conn)' is interpreted as 'create_account(event, ret, conn)'
        request = event.get("request_type")
        switch[request](event, ret, conn)

    return {
        'statusCode': ret.get('statusCode'),
        'body': json.dumps(ret.get('body'))
    }