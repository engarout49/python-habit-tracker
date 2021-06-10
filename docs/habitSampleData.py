# Import Required Modules
import habitTracker
import random
import habitDatabaseConnection
import psycopg2
import datetime
import time

# Function Area
def CreateWeeklySampleData(habitId):
        connection = habitDatabaseConnection.connect()
        tempCursor = connection.cursor()
        sqlQuery = 'INSERT INTO public."HabitHistory"("HabitId", "Date") VALUES (''%s'', ''%s'');'
        tempCursor.execute(sqlQuery, (str(habitId), '2021-05-01'))
        tempCursor.execute(sqlQuery, (str(habitId), '2021-05-07'))
        tempCursor.execute(sqlQuery, (str(habitId), '2021-05-021'))
        connection.commit()

def CreateDailySampleData(habitId):
    usedInts = []
    usedInts.append(0)
    ranges = random.randint(95, 120)
    for x in range(ranges):
        backInDays = random.choice([i for i in range(1,120) if i not in usedInts])
        usedInts.append(backInDays)
        connection = habitDatabaseConnection.connect()
        tempCursor = connection.cursor()
        currentDate = datetime.date.today()
        finalDate = currentDate + datetime.timedelta(days=(-backInDays))
        finalDateAsString = datetime.datetime.strftime(finalDate, "%Y-%m-%d")
        currentDateAsString = datetime.date.today().strftime("%Y-%m-%d")
                        
        sqlQuery = 'INSERT INTO public."HabitHistory"("HabitId", "Date") VALUES (''%s'', ''%s'');'
        tempCursor.execute(sqlQuery, (str(habitId), str(finalDateAsString)))
        connection.commit()    
    usedInts.clear()

def main():
    # Create Example Habits
    # Daily Examples
    print('Create Daily Habits')
    dailyHabitList = []
    dailyHabitList.append(habitTracker.Habit(0, 'Wake Up At 6AM', 'DAILY', True))
    dailyHabitList.append(habitTracker.Habit(0, 'Do 30 Minutes Sports', 'DAILY', True))
    dailyHabitList.append(habitTracker.Habit(0, 'Do Meditation', 'DAILY', True))
    dailyHabitList.append(habitTracker.Habit(0, 'Eat a Healthy Meal', 'DAILY', True))

    x = 0
    while x < len(dailyHabitList):
        habitId = habitTracker.NewHabit(dailyHabitList[x].name, dailyHabitList[x].periodicity)
        dailyHabitList[x].id = habitId
        CreateDailySampleData(habitId)

        x += 1

    # Weekly Examples
    weeklyHabitList = []
    weeklyHabitList.append(habitTracker.Habit(0, 'Read a Book', 'WEEKLY', True))

    habitId = habitTracker.NewHabit(weeklyHabitList[0].name, weeklyHabitList[0].periodicity)
    weeklyHabitList[0].id = habitId
    CreateWeeklySampleData(habitId)

    # Create Example History Data -> Contains only the past 4 weeks
