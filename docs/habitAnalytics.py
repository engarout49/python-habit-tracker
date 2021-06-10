# Import Required Packages
import psycopg2
import datetime
import habitDatabaseConnection
import habitTracker

# Function to Return List of Currently Tracked Habits
def ListTrackedHabits():
    # Function to Retrieve Habits
    def RetrieveHabits():
        sqlQuery = 'SELECT "Id", "Name", "Periodicity", "Active" FROM public."Habit" WHERE "Active" = true;'
        tempHabitList = []

        tempCursor = connection.cursor()
        tempCursor.execute(sqlQuery)
        tempResults = tempCursor.fetchall()

        for result in tempResults:
            tempHabitList.append(habitTracker.Habit(result[0],result[1],result[2],result[3]))
        
        return tempHabitList

    connection = habitDatabaseConnection.connect()

    # Define empty List and Insert Habits Retrieved from Function
    nonCommitHabitList = []
    nonCommitHabitList = RetrieveHabits()

    if not nonCommitHabitList:
        print('Habit list is empty!')
    else:
        print('Currently tracked habits:')
        print('--------------------------')

        for habit in nonCommitHabitList:
            print('Id: '
                + str(habit.id)
                + ' Habit: '
                + habit.name
                + ' Periodicity: '
                + habit.periodicity)

        return nonCommitHabitList

def ListHabitsPerPeriodicity(periodicity):
        # Function to Retrieve Habits
    def RetrieveHabits(periodicity):
        sqlQuery = ('SELECT "Id", "Name", "Periodicity", "Active" FROM public."Habit" WHERE "Periodicity" = '
                    + '\''
                    + periodicity
                    + '\';')
        # Define empty List and Insert Habits Retrieved from Function
        tempHabitList = []

        connection = habitDatabaseConnection.connect()

        tempCursor = connection.cursor()
        tempCursor.execute(sqlQuery)
        tempResults = tempCursor.fetchall()

        for result in tempResults:
            tempHabitList.append(habitTracker.Habit(result[0],result[1],result[2],result[3]))
        
        return tempHabitList
    def PrintHabits(habitList):
        print('Currently tracked habits:')
        print('--------------------------')

        for habit in habitList:
            print('Id: '
                + str(habit.id)
                + ' Habit: '
                + habit.name
                + ' Periodicity: '
                + habit.periodicity)

    if periodicity == 'DAILY':
        print('DAILY')
        tempHabitList = RetrieveHabits(('DAILY'))
        if not tempHabitList:
            print('Habit list is empty!')
        else:
            PrintHabits(tempHabitList)
            return tempHabitList
    elif periodicity == 'WEEKLY':
        print('WEEKLY')
        tempHabitList = RetrieveHabits(('WEEKLY'))
        if not tempHabitList:
            print('Habit list is empty!')
            return None
        else:
            PrintHabits(tempHabitList)
            return tempHabitList
    else:
        print('Periodicity not found!')
        return None

def GetLongestStreak(habit):
    def GetMarkedData(habitId):
        localHabitId = habitId
        sqlQuery = 'SELECT "Date" FROM public."HabitHistory" WHERE "HabitId" = ' + localHabitId + ' ORDER BY "Date";'
        tempCursor = connection.cursor()
        tempCursor.execute(sqlQuery, (str(localHabitId)))
        tempResults = tempCursor.fetchall()
        return tempResults

    connection = habitDatabaseConnection.connect()
    if habit.periodicity == 'DAILY':
        # Set Streak and Highest Streak
        # Streak is used to store the actual streak
        # HighestStreak is used to store the highest streak
        streak = 0
        highestStreak = 0

        habitHistory = GetMarkedData(str(habit.id))
        # LastMarkedDate is used to store the latest checked date
        lastStreak = None

        for entry in habitHistory:
            # Format iterator entry to proper datetime format
            formattedEntry = datetime.datetime.combine(entry[0], datetime.datetime.min.time())

            # Check if initial set of lastMarkedDate is required
            if lastStreak is None:
                lastStreak = formattedEntry
                streak += 1
            else:
                if (lastStreak + datetime.timedelta(days=1)) == formattedEntry:
                    lastStreak = formattedEntry
                    streak += 1
                else:
                    lastStreak = formattedEntry
                    streak = 0

            if streak > highestStreak:
                highestStreak = streak
        
        return highestStreak

    elif habit.periodicity == 'WEEKLY':
        # Set Streak and Highest Streak
        # Streak is used to store the actual streak
        # HighestStreak is used to store the highest streak
        streak = 0
        highestStreak = 0
        habitHistory = GetMarkedData(str(habit.id))
        # LastMarkedDate is used to store the latest checked date
        lastMarkedDate = None

        for entry in habitHistory:
            # Format iterator entry to proper datetime format
            formattedEntry = datetime.datetime.combine(entry[0], datetime.datetime.min.time())

            # Check if initial set of lastMarkedDate is required
            if lastMarkedDate is None:
                lastMarkedDate = formattedEntry
                streak += 1
            else:
                # Set EndDate to LastMarkedDate plus 13 Days, to also cover days behind the last marked date f.e. if the habit has been checked on Monday, we also want to cover the days after Monday the coming week
                endDate = lastMarkedDate + datetime.timedelta(days=13)

                if lastMarkedDate <= formattedEntry <= endDate:
                    lastMarkedDate = formattedEntry
                    streak += 1
                else:
                    lastMarkedDate = formattedEntry
                    streak = 0
                if streak > highestStreak:
                    highestStreak = streak

        return highestStreak

    else:
        print('Cannot found Periodicity')
        return None

def GetLongestStreakAllHabits():
    def RetrieveHabits():
        sqlQuery = 'SELECT "Id", "Name", "Periodicity", "Active" FROM public."Habit" WHERE "Active" = true;'
        tempHabitList = []

        tempCursor = connection.cursor()
        tempCursor.execute(sqlQuery)
        tempResults = tempCursor.fetchall()

        for result in tempResults:
            tempHabitList.append(habitTracker.Habit(result[0],result[1],result[2],result[3]))
        
        return tempHabitList
    def GetMarkedData(habitId):
        localHabitId = habitId
        sqlQuery = 'SELECT "Date" FROM public."HabitHistory" WHERE "HabitId" = ' + localHabitId + ' ORDER BY "Date";'
        tempCursor = connection.cursor()
        tempCursor.execute(sqlQuery, (str(localHabitId)))
        tempResults = tempCursor.fetchall()
        return tempResults

    connection = habitDatabaseConnection.connect()

    # Define empty List and Insert Habits Retrieved from Function
    nonCommitHabitList = []
    nonCommitHabitList = RetrieveHabits()

    highestStreak = 0
    highestStreakHabit = None

    for habit in nonCommitHabitList:
        if habit.periodicity == 'DAILY':
            # Set Streak and Highest Streak
            # Streak is used to store the actual streak
            # HighestStreak is used to store the highest streak
            streak = 0

            habitHistory = GetMarkedData(str(habit.id))
            # LastMarkedDate is used to store the latest checked date
            lastStreak = None

            for entry in habitHistory:
                # Format iterator entry to proper datetime format
                formattedEntry = datetime.datetime.combine(entry[0], datetime.datetime.min.time())

                # Check if initial set of lastMarkedDate is required
                if lastStreak is None:
                    lastStreak = formattedEntry
                    streak += 1
                else:
                    if (lastStreak + datetime.timedelta(days=1)) == formattedEntry:
                        lastStreak = formattedEntry
                        streak += 1
                    else:
                        lastStreak = formattedEntry
                        streak = 0

                if streak > highestStreak:
                    highestStreak = streak
                    highestStreakHabit = habit
            
        elif habit.periodicity == 'WEEKLY':
            # Set Streak and Highest Streak
            # Streak is used to store the actual streak
            # HighestStreak is used to store the highest streak
            streak = 0

            habitHistory = GetMarkedData(str(habit.id))
            # LastMarkedDate is used to store the latest checked date
            lastMarkedDate = None

            for entry in habitHistory:
                # Format iterator entry to proper datetime format
                formattedEntry = datetime.datetime.combine(entry[0], datetime.datetime.min.time())

                # Check if initial set of lastMarkedDate is required
                if lastMarkedDate is None:
                    lastMarkedDate = formattedEntry
                    streak += 1
                else:
                    # Set EndDate to LastMarkedDate plus 13 Days, to also cover days behind the last marked date f.e. if the habit has been checked on Monday, we also want to cover the days after Monday the coming week
                    endDate = lastMarkedDate + datetime.timedelta(days=13)

                    if lastMarkedDate <= formattedEntry <= endDate:
                        lastMarkedDate = formattedEntry
                        streak += 1
                    else:
                        lastMarkedDate = formattedEntry
                        streak = 0
                    if streak > highestStreak:
                        highestStreak = streak
                        highestStreakHabit = habit

    return highestStreak, highestStreakHabit