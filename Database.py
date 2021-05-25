#\ This is the function for the (PostgreSQL)database in Heroku
#\ reference :
#\  - https://ithelp.ithome.com.tw/articles/10219773
#\  - https://learningsky.io/database-pgadmin-postgresql-heroku/
#\
import os
import psycopg2
import urllib.parse as urlparse
from VarIndex import *


#\ Init the database info
def InitDBInfo()->dict:
    print("[INFO] Init the DB info")
    try:
        try:
            #\ Actually just replace the os.popen to os.environ
            # PG_DATABASE_URL = os.environ['DATABASE_URL']
            #\ This is for the heroku deploy
            PG_DATABASE_URL = urlparse.urlparse(os.environ['DATABASE_URL'])

            #\ Catrgorize the option
            dbname = PG_DATABASE_URL.path[1:]
            user = PG_DATABASE_URL.username
            password = PG_DATABASE_URL.password
            host = PG_DATABASE_URL.hostname
            port = PG_DATABASE_URL.port
            print("[INFO] Init the DB info successfully(os.environ)")
            return {"dbname":dbname, "user":user, "password":password, "host":host, "port":port}

        except:
            #\ This is for the local
            PG_DATABASE_URL = os.popen('heroku config:get DATABASE_URL -a dragonfly-flask-web').read()[:-1]
            print("[INFO] Init the DB info successfully(os.popen)")
            return {"DBURI":PG_DATABASE_URL}

    except :
        print("[Warning] Init the DB information fail")
        return None




#\ craete database connection
def CreateDBConection():
    print("[INFO] Start to CreateDBConection")

    try:
        # conn = psycopg2.connect(PG_DATABASE_URL, sslmode='require')
        # PG_DATABASE_URL = urlparse.urlparse(os.environ['DATABASE_URL'])
        # dbname = PG_DATABASE_URL.path[1:]
        # user = PG_DATABASE_URL.username
        # password = PG_DATABASE_URL.password
        # host = PG_DATABASE_URL.hostname
        # port = PG_DATABASE_URL.port
        # conn = psycopg2.connect(
        #         dbname=dbname,
        #         user=user,
        #         password=password,
        #         host=host,
        #         port=port
        #         )
        try:
            # print(cache.get("DBInfo"))
            conn = psycopg2.connect(**cache.get("DBInfo"), sslmode='require')
        except:
            conn = psycopg2.connect(cache.get("DBInfo")["DBURI"], sslmode='require')#\ This is for the local DB connection

        print("[INFO] Successfully create the connection to the database")
        return conn

    except:
        print("[WARNING] Unable to create the connection to the database")
        return None


#\ Execute the SQL command
def ExecuteDB(conn, query):
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        print("[INFO] Successfully execute the database query")
        return cursor

    except:
        print("[WARNING] Unable to execute the database query")
        return None


#\ Insert into DB SQL command
def InsertDB(conn, query, data):
    try:
        cursor = conn.cursor()
        cursor.execute(query, data)
        conn.commit()
        print("[INFO] Successfully execute the insert database query")

    except:
        print("[WARNING] Unable to execute the insert database query")


#\ Update
def UpdateDB(conn, query, data):
    pass


#\ Read the data
def ReadFromDB(conn, query, FetchOneOrNot)->tuple:
    cursor = ExecuteDB(conn, query)
    if FetchOneOrNot:
        print(f"[INFO] Read from DB : \n{cursor.fetchall()}")
        return cursor.fetchone()
    else:
        print(f"[INFO] Read from DB : \n{cursor.fetchall()}")
        return cursor.fetchall()


#\ Close the DB connection
def CloseDBConnection(conn):
    try:
        cursor = conn.cursor()
        cursor.close()
        conn.close()
        print("[INFO] Successfully close the database connection")

    except:
        print("[WARNING] Unable to close the database connection")


###################################################################################################
#\ --- SQL query ---

#\ Create data base
#\  SERIAL : is not a true data type, but is simply shorthand notation that tells Postgres to create a auto incremented,
#\              unique identifier for the specified column.
UserInfo_create_table_query = '''CREATE TABLE IF NOT EXISTS UserInfo(
    record_no serial PRIMARY KEY 1,
    name VARCHAR (50) NOT NULL,
    userid VARCHAR (50) PRIVATE NOT NULL,
    join_date DATE NOT NULL,
    account VARCHAR (50) NOT NULL,
    password VARCHAR (50) NOT NULL
);'''


#\ Insert query
#\ i.e. INSERT INTO products (product_no, name, price) VALUES (1, 'Cheese', 9.99);
Insert_query = lambda Table, name, value : f"INSERT INTO {Table} {name} VALUES {value};"

#\ insert to the userinfo database if the userid conflict then update the reset of the column
#\ value should be "(XXX, XXX, XXXX, XX, XXXXX, .....)"
Insert_userinfo_query = lambda Table : f"INSERT INTO {Table} (name, userid, join_date, account, password) VALUES (%s, %s, %s, %s, %s) ON CONFLICT ON CONSTRAINT userinfo_userid_key DO UPDATE SET name = EXCLUDED.name, join_date=EXCLUDED.join_date, account=EXCLUDED.account, password=EXCLUDED.password ;"


#\ Read the userinfo
Read_userinfo_query = lambda Table, userid : f"SELECT * FROM {Table} WHERE userid = '{userid}';"

#\ -- For testing --

