#\ This is the function for the (PostgreSQL)database in Heroku
#\ reference :
#\  - https://ithelp.ithome.com.tw/articles/10219773
#\  - https://learningsky.io/database-pgadmin-postgresql-heroku/
#\
import os
import psycopg2

DATABASE_URL = os.popen('heroku config:get DATABASE_URL -a dragonfly-flask-web').read()[:-1]

#\ craete database connection
def CreateDBConection():
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        print("[INFO] Successfully create the connection to the database")
        return conn

    except:
        print("[WARNING] Unabnle to create the connection to the database")
        return None


#\execute the SQL command
def ExecuteDB(conn, query):
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        print("[INFO] Successfully execute the database query")

    except:
        print("[WARNING] Unable to execute the database query")


#\ close the DB connection
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
def Insert_userinfo_query(Table:str, name:str,  userid:str, join_date:str, account:str, password:str):
    return f"""INSERT INTO {Table} (name, userid, join_date, account, password) VALUES ('{name}', '{userid}', '{join_date}', '{account}', '{password}') ON CONFLICT ON CONSTRAINT userinfo_userid_key DO UPDATE SET name = EXCLUDED.name, join_date=EXCLUDED.join_date, account=EXCLUDED.account, password=EXCLUDED.password ;"""
