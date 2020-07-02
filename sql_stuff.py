import psycopg2
import pandas as pd
import multiscript_config as msc

connection = psycopg2.connect( host = msc.DB_URL, port = msc.DB_PORT, user = msc.DB_USERNAME,
    password = msc.DB_PASSWORD, database = msc.DB_NAME )
cursor = connection.cursor()

def getTagsofEmailsCombined(conn) :
    list_email_tag_strength = []
    cur = conn.cursor()
    cur.execute( """SELECT DISTINCT users.email, users.first_name
                    FROM ((strength_analysis INNER JOIN quiz_submissions ON strength_analysis.submission_id = quiz_submissions.id)
                    INNER JOIN users ON users.id = quiz_submissions.user_id)""" )
    for emailid in cur.fetchall() :
        dict_user = {}
        dict_user.__setitem__('email', emailid[0]) 
        dict_user.__setitem__('first_name', emailid[1]) 
        print(f'\n EMAIL : {emailid[0]}\nFIRST_NAME : {emailid[1]}')
        cur.execute("""SELECT DISTINCT strength_analysis.tag,  strength_analysis.strength
                        FROM ((users INNER JOIN quiz_submissions ON users.id = quiz_submissions.user_id)
                        INNER JOIN strength_analysis ON strength_analysis.submission_id = quiz_submissions.id) WHERE users.email = '{}'""".format(emailid[0]) )
        for tag in cur.fetchall() :
            dict_user.__setitem__(tag[0], tag[1])
        print(f'dict_user :\n{dict_user}')
        list_email_tag_strength.append(dict_user)
    return list_email_tag_strength

list_of_dicts = getTagsofEmailsCombined(connection)