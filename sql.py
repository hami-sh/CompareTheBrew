import os.path
from os import path
import psycopg2
import sqlite3

def sqlhandler(list, mode):
    # check if file present
    if path.exists('drinks.db') == False:
        # use SQLite3 to create the database (not recommended in postgresql)
        conn = sqlite3.connect('drinks.db')
        c = conn.cursor()
        conn.commit()
        conn.close()

    # append or update mode
    if mode == "append":
        # insert into table
        try:
            connection = psycopg2.connect(user="sysadmin",
                                          password="pynative@#29",
                                          host="127.0.0.1",
                                          port="5432",
                                          database="drinks.db")

            cursor = connection.cursor()
            # Print PostgreSQL Connection properties
            print(connection.get_dsn_parameters(), "\n")

            # Print PostgreSQL version
            cursor.execute("SELECT version();")
            record = cursor.fetchone()
            print("You are connected to - ", record, "\n")

        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)
        finally:
            # closing database connection.
            if (connection):
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")

    elif mode == "update":
        # update entries with the same name / add entries who's names do not exist.
        print(1)




