import psycopg2
import pandas as pd
import multiscript_config as msc

connection = psycopg2.connect( host = msc.DB_URL, port = msc.DB_PORT, user = msc.DB_USERNAME,
    password = msc.DB_PASSWORD, database = msc.DB_NAME )
cursor = connection.cursor()

def doQuery(conn) :
    cur = conn.cursor()
    cur.execute( """SELECT DISTINCT users.email 
                    FROM ((strength_analysis INNER JOIN quiz_submissions ON strength_analysis.submission_id = quiz_submissions.id)
                    INNER JOIN users ON users.id = quiz_submissions.user_id)""" )
    for email in cur.fetchall() :
        print(email)

doQuery(connection) # Gets email of each user