#\ This is the function for the (PostgreSQL)database in Heroku / Render
import os
import psycopg2
import urllib.parse as urlparse
from VarIndex import *
import index
import csv

def InitDBInfo()->dict:
    print("[INFO] Init the DB info")
    try:
        db_url = os.environ.get('DATABASE_URL')
        if not db_url:
            print("[Warning] DATABASE_URL environment variable is not set.")
            return None

        PG_DATABASE_URL = urlparse.urlparse(db_url)
        dbname = PG_DATABASE_URL.path[1:]
        user = PG_DATABASE_URL.username
        password = PG_DATABASE_URL.password
        host = PG_DATABASE_URL.hostname
        port = PG_DATABASE_URL.port
        print("[INFO] Init the DB info successfully(os.environ)")
        return {"dbname":dbname, "user":user, "password":password, "host":host, "port":port}
    except Exception as e:
        print(f"[Warning] Init the DB information fail: {e}")
        return None

def CreateDBConection():
    print("[INFO] Start to CreateDBConection")
    try:
        db_info = cache.get("DBInfo")
        if db_info and "dbname" in db_info:
            conn = psycopg2.connect(**db_info, sslmode='require')
        else:
            DbInfo = InitDBInfo()
            if DbInfo:
                conn = psycopg2.connect(**DbInfo, sslmode='require')
            else:
                conn = None
                print("[WARNING] Unable to create the connection to the database")
        print("[INFO] Successfully create the connection to the database")
        return conn
    except Exception as e:
        print(f"[WARNING] Unable to create the connection to the database: {e}")
        return None

def ExecuteDB(conn, query):
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        print("[INFO] Successfully execute the database query")
        return cursor
    except Exception as e:
        print(f"[WARNING] Unable to execute the database query: {e}")
        if conn:
            conn.rollback()
        return None

def InsertDB(conn, query:str, data:tuple, close_connection:bool=False)->bool:
    try:
        cursor = conn.cursor()
        cursor.execute(query, data)
        conn.commit()
        print("[INFO] Successfully execute the insert database query")
        Staus = True
    except Exception as e:
        print(f"[WARNING] Unable to execute the insert database query: {e}")
        if conn:
            conn.rollback()
        Staus = False

    if close_connection:
        CloseDBConnection(conn)
    return Staus

def InsertManyDB(conn, query, datas, close_connection=False):
    try:
        for data in datas:
            cursor = conn.cursor()
            cursor.execute(query, data)
            conn.commit()
            print(f"[INFO] Successfully execute the {data} insert database query")
    except Exception as e:
        print(f"[WARNING] Unable to execute the insert database query: {e}")
        if conn:
            conn.rollback()
    if close_connection:
        CloseDBConnection(conn)

def UpdateDB(conn, query, data):
    pass

def ReadFromDB(conn, query, FetchOneOrNot=True, CloseConn=False):
    cursor = ExecuteDB(conn, query)
    try:
        if cursor is None:
            return None

        if FetchOneOrNot:
            returnData = cursor.fetchone()
        else:
            returnData = cursor.fetchall()

        if CloseConn is True:
            CloseDBConnection(conn)

        return returnData
    except Exception as e:
        print(f"[Warning] Read from DB might not have the data or something wrong: {e}")
        return None

def CloseDBConnection(conn):
    try:
        cursor = conn.cursor()
        cursor.close()
        conn.close()
        print("[INFO] Successfully close the database connection")
    except:
        print("[WARNING] Unable to close the database connection")

def InitDatabaseForSpeciesFamily():
    pass

#\ --- 已修復所有語法錯誤的正統 PostgreSQL 語法 ---
UserInfo_create_table_query = '''CREATE TABLE IF NOT EXISTS UserInfo(
    record_no serial PRIMARY KEY,
    name VARCHAR (50) NOT NULL,
    userid VARCHAR (50) UNIQUE NOT NULL,
    join_date DATE NOT NULL,
    account VARCHAR (50) NOT NULL,
    password VARCHAR (50) NOT NULL,
    current_crawling_id VARCHAR (50),
    access_token VARCHAR (50)
);'''

Variable_create_table_query = '''CREATE TABLE IF NOT EXISTS Variable(
    variable_no serial PRIMARY KEY,
    var_name VARCHAR (50) NOT NULL,
    var_value VARCHAR (50) NOT NULL
);'''

Read_all_query = lambda Table : f"SELECT * FROM {Table}"
Insert_query = lambda Table, name, value : f"INSERT INTO {Table} {name} VALUES {value};"
Insert_userinfo_query = lambda: f"INSERT INTO {index.UserInfoTableName} (name, userid, join_date, account, password) VALUES (%s, %s, %s, %s, %s) ON CONFLICT (userid) DO UPDATE SET name = EXCLUDED.name, join_date=EXCLUDED.join_date, account=EXCLUDED.account, password=EXCLUDED.password;"
Read_userinfo_query = lambda userid : f"SELECT * FROM {index.UserInfoTableName} WHERE userid = '{userid}';"
Read_col_userinfo_query = lambda Col, userid : f"SELECT {Col} FROM {index.UserInfoTableName} WHERE userid = '{userid}';"
Read_all_row_for_col_query = lambda Col_name : f"SELECT {Col_name} FROM {index.UserInfoTableName};"
Update_userinfo_query = lambda column_name: f"UPDATE {index.UserInfoTableName} SET {column_name}=%s WHERE userid=%s;"
Insert_variable_query =  lambda Table : f"INSERT INTO {Table} (var_name, var_value) VALUES (%s, %s)"
Read_variable_query = lambda var_name : f"SELECT * FROM {index.VariableTableName} WHERE var_name = '{var_name}';"
Update_varaible_query = f"UPDATE {index.VariableTableName} SET var_value=%s WHERE var_name=%s;"