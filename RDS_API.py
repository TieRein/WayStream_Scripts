## Author: Jacob Chesley
##
## API structure for database calls
## Last Updated: 2/28/19

import json
import sys
import pymysql
import urllib2
import rds_config
import uuid

# For publishing to IOT Core topics
import boto3

# For salting a password
import os
import struct
import hashlib

# RDS settings
rds_host  = rds_config.db_rds_host
name = rds_config.db_username
password = rds_config.db_password
db_name = rds_config.db_name
salt_db_name = rds_config.salt_db_name
salt_count = rds_config.salt_count
confirmation_email_host = rds_config.confirmation_email_host

# IOT Core settings
region = rds_config.region
access_key = rds_config.access_key
secret_key = rds_config.secret_key


def make_secure_password(pass_return, ret):
    if pass_return['salt_id'] == 0:
        pass_return['salt_id'] = struct.unpack('>Q', os.urandom(8))[0] % salt_count + 1
    try:
        salt_db = pymysql.connect(rds_host, user=name, passwd=password, db=salt_db_name, connect_timeout=5)
        with salt_db.cursor() as salt_cur:
            salt_cur.execute("SELECT Salt_Data FROM Salt WHERE Salt_ID = %s;", pass_return['salt_id'])
            salt_password =  pass_return['password'] + str(salt_cur.fetchone())
            secure_password = hashlib.sha256(salt_password.encode())
            pass_return['password'] = secure_password.hexdigest()
    except:
        ret['statusCode'] = 400


def create_account(event, ret, conn):
    with conn.cursor() as cur:
        create = event.get("data")
        cur.execute("SELECT User_ID FROM User WHERE Username = %s;", create.get("username"))
        check_username = cur.fetchone()
        cur.execute("SELECT User_ID FROM User WHERE Email = %s;", create.get("email"))
        check_email = cur.fetchone()
        
        # Check to see if this account has unique identifiers
        if check_username != None and check_email != None:
            ret['statusCode'] = 403
            ret['body'] = "Username and Email already taken"
        elif check_username != None:
            ret['statusCode'] = 403
            ret['body'] = "Username already taken"
        elif check_email != None:
            ret['statusCode'] = 403
            ret['body'] = "Email already taken"
        else:
            try:
                pass_return = {'password': create.get("password"), 'salt_id': 0}
                make_secure_password(pass_return, ret)
                if ret['statusCode'] == 400:
                    raise Exception("Unable to access salt database")
                cur.execute("INSERT INTO User (First_Name, Last_Name, Email, Username, Secure_Password, Salt_ID) VALUES(%s, %s, %s, %s, %s, %s);", (create.get("f_name"), create.get("l_name"), create.get("email"), create.get("username"), pass_return['password'], pass_return['salt_id'],))
                conn.commit()
                cur.execute("SELECT User_ID FROM User WHERE Username = %s;", create.get("username"))
                account_id = cur.fetchone()[0]
                
                # Sends confirmation email to user
                # API call through API Gateway (sendConfirmationEmail) stage to (sendConfirmationEmail) Lambda function
                urllib2.urlopen("%semail=%s&username=%s&accountID=%s" % (confirmation_email_host, create.get("email"), create.get("username"), account_id))
                ret['statusCode'] = 200
                ret['body'] = "Successfully created account"
            except:
                ret['statusCode'] = 400
                ret['body'] = "Bad Request (TODO: Implement more fine grained error codes here)"


def login(event, ret, conn):
    with conn.cursor() as cur:
        account_login = event.get("data")
        cur.execute("SELECT * FROM User WHERE Username = %s;", account_login.get("username"))
        account_data = cur.fetchone()
        
        # If the username wasn't found, the user may have entered their email
        if account_data == None:
            cur.execute("SELECT * FROM User WHERE Email = %s;", account_login.get("username"))
            account_data = cur.fetchone()
            
        # If login still isn't found throw error
        if account_data == None:
            ret['statusCode'] = 403
            ret['body'] = "Account does not exist"
        else:
            pass_return = {'password': account_login.get("password"), 'salt_id': account_data[5]}
            make_secure_password(pass_return, ret)
            if pass_return['password'] != account_data[4]:
                ret['statusCode'] = 401
                ret['body'] = "Incorrect credentials"
            else:
                ret['statusCode'] = 200
                ret['body'] = "Success... TODO: Add user object once created"


def confirm_email(event, ret, conn):
    with conn.cursor() as cur:
        account_login = event.get("account_id")
        cur.execute("SELECT Confirmed_Email FROM WayStream_Prod.User WHERE User_ID=%s;", account_login)
        account_exists = cur.fetchone()
        if account_exists == None:
            ret['statusCode'] = 406
            ret['body'] = "Account does not exist"
        else:
            account = account_exists[0]
            if check == 1:
                ret['statusCode'] = 403
                ret['body'] = "Your email has already been confirmed"
            else:
                cur.execute("UPDATE WayStream_Prod.User SET Confirmed_Email=1 WHERE User_ID=%s;", account_login)
                conn.commit()
                ret['statusCode'] = 200
                ret['body'] = "Email successfully confirmed"


def get_system_history(event, ret, conn):
    with conn.cursor() as cur:
        system = event.get("system_id")
        cur.execute("SELECT * FROM WayStream_Prod.System_Runtime WHERE (Sys_ID = %s) AND (StopTime IS NOT NULL) ORDER BY Entry_Value;", system)
        data = cur.fetchall()
        json_data = {}
        for i,a in enumerate(data):
            json_data[i] = [a[2], a[3]]
        if data == None:
            ret['statusCode'] = 400
            ret['body'] = "System not found"
        else:
            ret['statusCode'] = 200
            ret['body'] = json.dumps(json_data)


def add_system_runtime(event, ret, conn):
    with conn.cursor() as cur:
        try:
            cur.execute("INSERT INTO Runtime_Event (Sys_ID, Runtime_ID, Runtime_Name, Color, Start_Year, Start_Month, Start_Day, Start_Hour, Start_Minute, End_Year, End_Month, End_Day, End_Hour, End_Minute) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", (event.get("system_id"), event.get("event_id"), event.get("event_name"), event.get("color"), event.get("start_year"), event.get("start_month"), event.get("start_day"), event.get("start_hour"), event.get("start_minute"), event.get("end_year"), event.get("end_month"), event.get("end_day"), event.get("end_hour"), event.get("end_minute"),))
            conn.commit()
            # Notifies the system that its events have been updated
            client = boto3.client('iot-data', region_name=region, aws_access_key_id=access_key, aws_secret_access_key=secret_key)
            client.publish(topic="Event_Update", qos=1, payload=json.dumps({"command": "Manual_Update"}))
            ret['statusCode'] = 200
            ret['body'] = "Successfully added runtime"
        except:
            ret['statusCode'] = 400
            ret['body'] = "Bad Request (TODO: Implement more fine grained error codes here)"


def get_system_runtime(event, ret, conn):
    with conn.cursor() as cur:
        system = event.get("system_id")
        cur.execute("SELECT * FROM WayStream_Prod.Runtime_Event WHERE Sys_ID = %s;", system)
        data = cur.fetchall()
        json_data = {}
        for i,a in enumerate(data):
            print a
            json_data[i] = a
        if data == None:
            ret['statusCode'] = 400
            ret['body'] = "System not found"
        else:
            ret['statusCode'] = 200
            ret['body'] = json.dumps(json_data)


def lambda_handler(event, context):
    # List of functions that may be called
    ret = {'statusCode': -1, 'body': -1}
    switch={'create_account': create_account, 'login': login, 'confirm_email': confirm_email, 'get_system_history': get_system_history, 'add_system_runtime': add_system_runtime, 'get_system_runtime': get_system_runtime}
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