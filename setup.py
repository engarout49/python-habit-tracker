import time
import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def checkRequiredModules():
    print("Checking Module: psycopg2")
    try:
        import psycopg2
        return True
    except ModuleNotFoundError:
        print("Module: psycopg2 not found")
        print("Installing...")
        install("psycopg2")
        return False

def checkDatabaseConnection(hostName, userName, passWord):
    print("Database Check")
    import psycopg2
    try:
        connection = psycopg2.connect(
                host=hostName,
                database='postgres',
                user=userName,
                password=passWord
            )
        cursor = connection.cursor()
        cursor.execute('SELECT version();')
        print("Connection Established")
        return True
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
        return False

def createDatabase(hostName, userName, passWord):
    import psycopg2
    try:
        connection = psycopg2.connect(
                host=hostName,
                database='postgres',
                user=userName,
                password=passWord
            )
        connection.autocommit = True
        cursor = connection.cursor()
        cursor.execute('CREATE DATABASE "PyHabitTracker" WITH  OWNER = ' + userName + ' ENCODING = ''UTF8'' TABLESPACE = pg_default  CONNECTION LIMIT = -1;')
        connection.commit()
        print('Database created')
        return True
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
        return False

def createTables(hostName, userName, passWord):
    import psycopg2
    try:
        connection = psycopg2.connect(
                host=hostName,
                database='PyHabitTracker',
                user=userName,
                password=passWord
            )
        connection.autocommit = True
        cursor = connection.cursor()
        cursor.execute('CREATE SEQUENCE public."Habit_Id_seq" INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1; ALTER SEQUENCE public."Habit_Id_seq" OWNER TO postgres; CREATE TABLE public."Habit" ( "Id" bigint NOT NULL DEFAULT nextval(\'\"Habit_Id_seq\"\'::regclass), "Name" character varying COLLATE pg_catalog."default" NOT NULL, "Periodicity" character varying COLLATE pg_catalog."default" NOT NULL, "Active" boolean NOT NULL, "CreationDate" date NOT NULL, CONSTRAINT "Habit_pkey" PRIMARY KEY ("Id")) TABLESPACE pg_default; ALTER TABLE public."Habit" OWNER to postgres;')
        cursor.execute('CREATE SEQUENCE public."HabitHistory_Id_seq" INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1; ALTER SEQUENCE public."HabitHistory_Id_seq" OWNER TO postgres; CREATE SEQUENCE public."HabitHistory_HabitId_seq" INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1; ALTER SEQUENCE public."HabitHistory_HabitId_seq" OWNER TO postgres; CREATE TABLE public."HabitHistory" ("Id" bigint NOT NULL DEFAULT nextval(\'\"HabitHistory_Id_seq\"\'::regclass), "HabitId" bigint NOT NULL DEFAULT nextval(\'\"HabitHistory_HabitId_seq\"\'::regclass), "Date" date NOT NULL, CONSTRAINT "HabitHistory_pkey" PRIMARY KEY ("Id")) TABLESPACE pg_default; ALTER TABLE public."HabitHistory" OWNER to postgres;')
        print('Tables created')
        return True
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
        return False
def main():
    print("PyHabit Installation Routine")
    print("----------------------------")
    
    # Steps for Required Modules
    time.sleep(0.5)
    counter = 0
    while checkRequiredModules() == False:
        print("Checking Required Modules")
        time.sleep(2)
        counter = counter + 1
        if counter is 5:
            print("Tried to install 5 times, installation will be cancelled.")
            time.sleep(0.5)
            exit()
    print("Required Modules Checked")

    # Steps for Database
    print('Create Database and Tables')
    #databaseHost = input("Please enter the database host:")
    #databaseUsername = input("Please enter a database user:")
    #databasePassword = input("Please enter the password for the above user:")
    databaseHost = 'localhost'
    databaseUsername = 'postgres'
    databasePassword = 'python'

    checkDatabaseConnection(databaseHost, databaseUsername, databasePassword)

    print('Create related Database')
    if createDatabase(databaseHost, databaseUsername, databasePassword) == False:
        exit()
    print('Create related Tables')
    if createTables(databaseHost, databaseUsername, databasePassword) == False:
        exit()

    # Steps for Example Data
    print('Create Sample Data')
    import habitSampleData
    habitSampleData.main()

    # Final Statement
    print('PyHabitTracker has been sucessfully installed!')
    print('To execute, run main.py from program folder.')

# Run Main
if __name__ == "__main__":
    main()