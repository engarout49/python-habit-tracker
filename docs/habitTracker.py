# Import required packages
import psycopg2
import datetime
import habitDatabaseConnection

# Python Habit Tracker
class Habit:    
    def __init__(self, id, name, periodicity, active):
        self.id = id
        self.name = name
        self.periodicity = periodicity
        self.active = active
    def MarkDone(self):
        habitId = self.id
        sqlQuery = 'SELECT "Date" FROM public."HabitHistory" WHERE "HabitId" = ' + str(habitId) + ' ORDER BY 1 DESC;'

        connection = habitDatabaseConnection.connect()
        tempCursor = connection.cursor()
        tempCursor.execute(sqlQuery)
        results = tempCursor.fetchall()
        currentDate = datetime.date.today()
        currentDateAsString = currentDate.strftime("%Y-%m-%d")

        if len(results) != 0:
            latestMarkDate = results[0]
            if latestMarkDate[0] != currentDate:
                sqlQuery = 'INSERT INTO public."HabitHistory"("HabitId", "Date") VALUES (\'' + str(habitId) + '\', \'' + str(currentDateAsString) + '\');'

                tempCursor.execute(sqlQuery)
                connection.commit()
                return True
            else:
                return False
        else:
            sqlQuery = 'INSERT INTO public."HabitHistory"("HabitId", "Date") VALUES (\'' + str(habitId) + '\', \'' + str(currentDateAsString) + '\');'

            tempCursor.execute(sqlQuery)
            connection.commit()
            return True


    def Edit(self, newName, newPeriodcity):
        def UpdateHabit(id, name, periodicity):
            if id is not None:
                if name is not None:
                    if periodicity is not None:
                            sqlQuery = 'UPDATE public."Habit" SET "Name"=''%s'', "Periodicity"=''%s'', "Active"=True WHERE "Id" = ''%s'';'

                            tempCursor = connection.cursor()
                            tempCursor.execute(sqlQuery, (name, periodicity, id))
                            connection.commit()

                            return tempCursor.statusmessage

        tempInputName = newName
        tempPeriodicity = newPeriodcity

        # Check for right Periodicity
        if tempPeriodicity == 'DAILY' or tempPeriodicity == 'WEEKLY':
            connection = habitDatabaseConnection.connect()
            updateCheck = UpdateHabit(self.id, tempInputName, tempPeriodicity)

            if updateCheck == "UPDATE 1" or updateCheck == "UPDATE 0":
                return True
            else:
                return False
        else: 
            return False

    def Unpublish(self):
        sqlQuery = 'UPDATE public."Habit" SET "Active"=false WHERE "Id" = %s;'

        connection = habitDatabaseConnection.connect()
        tempCursor = connection.cursor()
        tempCursor.execute(sqlQuery, str(self.id))
        connection.commit()

        return True

# Get Habits from Database
def SyncHabits():
    sqlQuery = 'SELECT "Id", "Name", "Periodicity", "Active" FROM public."Habit" WHERE "Active" = true;'
    habitList = []

    connection = habitDatabaseConnection.connect()
    tempCursor = connection.cursor()
    tempCursor.execute(sqlQuery)
    results = tempCursor.fetchall()

    for result in results:
        habitList.append(Habit(result[0],result[1],result[2],result[3]))
    
    return habitList
    
def ListHabits(habitList):
    for row in habitList:
        row.printOverview()

def NewHabit(name, periodicity):
    sqlQuery = 'INSERT INTO public."Habit"("Name", "Periodicity", "Active", "CreationDate") VALUES (%s, %s, %s, %s) RETURNING "Id";'

    currentDate = datetime.date.today()
    currentDateAsString = datetime.date.today().strftime("%Y-%m-%d")

    connection = habitDatabaseConnection.connect()
    tempCursor = connection.cursor()
    tempCursor.execute(sqlQuery, (name,periodicity,'true',currentDateAsString))
    connection.commit()

    id = int(tempCursor.fetchone()[0])

    if id is not None:
        return id
    else:
        return None
    
def GetHabit(listOfHabits, id):
    for habit in listOfHabits:
        if habit.id is id:
            return habit
