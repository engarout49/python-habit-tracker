import psycopg2

def connect():
    connection = None
    try:
        connection = psycopg2.connect(
            host='LOCALHOST',
            database='PyHabitTracker',
            user='postgres',
            password='python'
        )
        cursor = connection.cursor()
        cursor.execute('SELECT version();')
        #print(cursor.fetchall())
        return connection
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)