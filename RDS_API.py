## Author: Jacob Chesley
##
## API structure for database calls
## Last Updated: 1/28/19

import json
import sys
import pymysql
import rds_config

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
        try:
            create = event.get("data")
            pass_return = {'password': create.get("password"), 'salt_id': 0}
            make_secure_password(pass_return, ret)
            if ret['statusCode'] == 400:
                raise Exception("Unable to access salt database")
            cur.execute("INSERT INTO User (First_Name, Last_Name, Email, Username, Secure_Password, Salt_ID) VALUES(%s, %s, %s, %s, %s, %s);", (create.get("f_name"), create.get("l_name"), create.get("email"), create.get("username"), pass_return['password'], pass_return['salt_id'],))
            conn.commit()
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
        print account_data
        pass_return = {'password': account_login.get("password"), 'salt_id': account_data[5]}
        make_secure_password(pass_return, ret)
        print pass_return
        if pass_return['password'] != account_data[4]:
            ret['statusCode'] = 403
            ret['body'] = "Incorrect credentials"
        else:
            ret['statusCode'] = 200
            ret['body'] = "Success... TODO: Add user object once created"


def testing(event, ret, conn):
    salt_db = pymysql.connect(rds_host, user=name, passwd=password, db=salt_db_name, connect_timeout=5)
    with salt_db.cursor() as cur:
        id = struct.unpack('>H', os.urandom(2))[0] % salt_count + 1
        cur.execute("SELECT Salt_Data FROM Salt WHERE Salt_ID = %s;", id)
    ret['statusCode'] = id
    ret['body'] = cur.fetchone()


def lambda_handler(event, context):
    # List of functions that may be called
    switch={'create_account': create_account, 'testing': testing, 'login': login}
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