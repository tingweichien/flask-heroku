#\ This is the function for the (PostgreSQL)database in Heroku
#\ reference :
#\  - https://ithelp.ithome.com.tw/articles/10219773
#\  - https://learningsky.io/database-pgadmin-postgresql-heroku/
#\
import os
import psycopg2
import urllib.parse as urlparse
from VarIndex import *
import index


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
    """
    return : conn or None
    """
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
        #\ for the clock.py program, since it run at itself, set this to reload the DBInfo


        try:
            try:
                conn = psycopg2.connect(**cache.get("DBInfo"), sslmode='require')
            except:
                DbInfo = InitDBInfo()
                if len(DbInfo) > 1:
                    conn = psycopg2.connect(**DbInfo, sslmode='require')
                elif len(DbInfo) == 1:
                    conn = psycopg2.connect(DbInfo["DBURI"], sslmode='require')
                else:
                    conn = None
                    print("[WARNING] Unable to create the connection to the database")
        except:
            conn = psycopg2.connect(cache.get("DBInfo")["DBURI"], sslmode='require')#\ This is for the local DB connection
            #conn = psycopg2.connect(DBURI, sslmode='require')#\ This is for the local DB connection

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
        CloseDBConnection(conn)
        return None



#\ Insert into DB SQL command
def InsertDB(conn, query:str, data:tuple):
    """[summary]

    Args:
        conn ([type]): connection for the database
        query (string): query(the column) to insert
        data (tuple): data to be insert
    """
    try:
        cursor = conn.cursor()
        cursor.execute(query, data)
        conn.commit()
        print("[INFO] Successfully execute the insert database query")

    except:
        print("[WARNING] Unable to execute the insert database query")
    CloseDBConnection(conn)


#\ Insert multi into DB SQL command
def InsertManyDB(conn, query, datas):
    try:
        for data in datas:
            cursor = conn.cursor()
            # cursor.executemant(query, datas) #--> too slow
            cursor.execute(query, data)
            conn.commit()
            print(f"[INFO] Successfully execute the {data} insert database query")

    except:
        print("[WARNING] Unable to execute the insert database query")
    CloseDBConnection(conn)


#\ Update
def UpdateDB(conn, query, data):
    pass


#\ Read the data
def ReadFromDB(conn, query, FetchOneOrNot=True, CloseConn=True):
    """
    @params
        conn : Connection
        query : query for reading the database
        FetchOneOrNot : (True to fetch one , False to fetch all)Whether to get one data or all the data from the database
        CloseConn :  Decides whether to close the database connection after reading

    @return
        fetchone : return tuple
        fetchall : return list of tuple
    """
    cursor = ExecuteDB(conn, query)
    try:
        if FetchOneOrNot:
            returnData = cursor.fetchone()
            print(f"[INFO] Read from DB fetchone: \n{returnData}")
        else:
            returnData = cursor.fetchall()
            print(f"[INFO] Read from DB fetchall: \n{returnData}")

        #\ Don't Close connection
        if CloseConn is True:
            CloseDBConnection(conn)

        return returnData

    except:
        print("[Warning] Read from DB might not have the data or something wrong")
        return None


#\ Close the DB connection
def CloseDBConnection(conn):
    try:
        cursor = conn.cursor()
        cursor.close()
        conn.close()
        print("[INFO] Successfully close the database connection")

    except:
        print("[WARNING] Unable to close the database connection")


#\ handle the variable store in the "Variable table" in database from list of tuple to dict
# def TupleList2Dict(list_tuple:list)->dict:
#     return_dict = dict()
#     for t in list_tuple:
#         return_dict = dict((k, v) for (k, v) in t)

#     print(f"[INFO]The result of transferring from list of tuple to dictionary is\n{return_dict}")
#     return return_dict






###################################################################################################
#\ --- SQL query ---

#\ Create data base table(user info)
#\  SERIAL : is not a true data type, but is simply shorthand notation that tells Postgres to create a auto incremented,
#\              unique identifier for the specified column.
UserInfo_create_table_query = '''CREATE TABLE IF NOT EXISTS UserInfo(
    record_no serial PRIMARY KEY 1,
    name VARCHAR (50) NOT NULL,
    userid VARCHAR (50) PRIVATE NOT NULL,
    join_date DATE NOT NULL,
    account VARCHAR (50) NOT NULL,
    password VARCHAR (50) NOT NULL,
    current_crawling_id VARCHAR (50),
    access_token VARCHAR (50),
);'''



#\ Create data base table(Variable)
#\ store the variable here
Variable_create_table_query = '''CREATE TABLE IF NOT EXISTS Variable(
    variable_no serial PRIMARY KEY,
    var_name VARCHAR (50) NOT NULL,
    var_value VARCHAR (50) NOT NULL
);'''


#\ Testing
#\ Execute create connection
# PG_DATABASE_URL = os.popen('heroku config:get DATABASE_URL -a dragonfly-flask-web').read()[:-1]
# conn = psycopg2.connect(PG_DATABASE_URL, sslmode='require')
# ExecuteDB(conn, UserInfo_create_table_query)



#\ Read all query
Read_all_query = lambda Table : f"SELECT * FROM {Table}"


#\ Insert query and Read query
#\ --- User info table ---
#\ i.e. INSERT INTO products (product_no, name, price) VALUES (1, 'Cheese', 9.99);
Insert_query = lambda Table, name, value : f"INSERT INTO {Table} {name} VALUES {value};"

#\ insert to the userinfo database if the userid conflict then update the reset of the column
#\ value should be "(XXX, XXX, XXXX, XX, XXXXX, .....)"
Insert_userinfo_query = f"INSERT INTO {index.UserInfoTableName} (name, userid, join_date, account, password) VALUES (%s, %s, %s, %s, %s) ON CONFLICT ON CONSTRAINT userinfo_userid_key DO UPDATE SET name = EXCLUDED.name, join_date=EXCLUDED.join_date, account=EXCLUDED.account, password=EXCLUDED.password ;"

#\ Read the userinfo
Read_userinfo_query = lambda userid : f"SELECT * FROM {index.UserInfoTableName} WHERE userid = '{userid}';"

#\ Read specific column from the userinfo by userid
Read_col_userinfo_query = lambda Col, userid : f"SELECT {Col} FROM {index.UserInfoTableName} WHERE userid = '{userid}';"

#\ Read some of the column for all the database.
Read_all_row_for_col_query = lambda Col_name : f"SELECT {Col_name} FROM {index.UserInfoTableName};"


#\ Update user info
Update_userinfo_query = lambda column_name: f"UPDATE {index.UserInfoTableName} SET {column_name}=%s WHERE userid=%s;"


#\ --- Variable table ---
#\ Insert
Insert_variable_query =  lambda Table : f"INSERT INTO {Table} (var_name, var_value) VALUES (%s, %s)"

#\ Read the userinfo
Read_variable_query = lambda var_name : f"SELECT * FROM {index.VariableTableName} WHERE var_name = '{var_name}';"

#\ Update
#\ i.e. UPDATE public.variable	SET var_value = '79166'	WHERE var_name = 'LatestDataID';
Update_varaible_query = lambda Table : f"UPDATE {Table} SET var_value=%s WHERE var_name=%s;"