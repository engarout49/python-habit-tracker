import habitDatabaseConnection
import habitTracker
import habitAnalytics

# Main
def main():
    Menu()

def ReturnToMenu():
    tempInput = input('Do you would like to return to the menu? (Y - Yes): ')
    if tempInput == 'Y' or tempInput == 'y':
        Menu()
    else:
        print('Input not known. Exit program.')
        exit()


def MenuNewHabit():
    def NewHabit():
        habitId = habitTracker.NewHabit(tempHabitName, tempHabitPeriodicity)
        if int(habitId) > 0:
            print('Habit: ' + tempHabitName + ' with Periodicity: ' + tempHabitPeriodicity + ' was sucessfully created with Id: ' + str(habitId))
        else:
            print('Habit could not be created.')

    #print('Not Implemented')
    tempHabitName = input('Please enter name of habit: ')
    tempHabitPeriodicity = input('Please outline periodicity (1 - Daily | 2- Weekly): ')

    if tempHabitPeriodicity == '1':
        tempHabitPeriodicity = 'DAILY'
        NewHabit()
    elif tempHabitPeriodicity == '2':
        tempHabitPeriodicity = 'WEEKLY'
        NewHabit()
    else:
        print('Choise could not be processed.')
        print('Creation of habit aborted.')
        Menu()


def MenuEditHabit():
    habitAnalytics.ListTrackedHabits()
    tempHabitIdInput = input('Please enter the habit id: ')
    if int(tempHabitIdInput) > 0:
        habitList = habitTracker.SyncHabits()
        targetHabit = habitTracker.GetHabit(habitList, int(tempHabitIdInput))

        tempHabitName = input('Please enter new name of habit: ')
        tempHabitPeriodicity = input('Please outline new periodicity (1 - Daily | 2- Weekly): ')

        if tempHabitPeriodicity == '1':
            tempHabitPeriodicity = 'DAILY'
            targetHabit.Edit(tempHabitName, tempHabitPeriodicity)
        elif tempHabitPeriodicity == '2':
            tempHabitPeriodicity = 'WEEKLY'
            targetHabit.Edit(tempHabitName, tempHabitPeriodicity)
        else:
            print('Choise could not be processed.')
            print('Edit of habit aborted.')
            Menu()
    else:
        print('Choise could not be processed.')
        print('Edit of habit aborted.')
        Menu()

def MenuMarkHabit():
    habitAnalytics.ListTrackedHabits()
    tempHabitIdInput = input('Please enter the habit id: ')
    if int(tempHabitIdInput) > 0:
        habitList = habitTracker.SyncHabits()
        targetHabit = habitTracker.GetHabit(habitList, int(tempHabitIdInput))
        targetHabit = targetHabit.MarkDone()
        if targetHabit:
            print('Habit marked as done.')
        else:
            print('Habit could not be marked as done.')
    else:
        print('Choise could not be processed.')
        print('Mark of habit aborted.')
        Menu()


def MenuUnpublishHabit():
    habitAnalytics.ListTrackedHabits()
    tempHabitIdInput = input('Please enter the habit id: ')
    if int(tempHabitIdInput) > 0:
        habitList = habitTracker.SyncHabits()
        targetHabit = habitTracker.GetHabit(habitList, int(tempHabitIdInput))
        targetHabit.Unpublish()
    else:
        print('Choise could not be processed.')
        print('Unpublish of habit aborted.')
        Menu()



def MenuListHabits():
    habitAnalytics.ListTrackedHabits()

def MenuListHabitsPeriodicity():
    tempHabitPeriodicity = input('Please outline periodicity (1 - Daily | 2- Weekly): ')
    if tempHabitPeriodicity == '1':
        tempHabitPeriodicity = 'DAILY'
        habitAnalytics.ListHabitsPerPeriodicity(tempHabitPeriodicity)
    elif tempHabitPeriodicity == '2':
        tempHabitPeriodicity = 'WEEKLY'
        habitAnalytics.ListHabitsPerPeriodicity(tempHabitPeriodicity)
    else:
        print('Choise could not be processed.')
        print('Listing of habits aborted.')
        Menu()


def MenuGetLongestStreakPerHabit():
    habitAnalytics.ListTrackedHabits()
    tempHabitIdInput = input('Please enter the habit id: ')
    if int(tempHabitIdInput) > 0:
        habitList = habitTracker.SyncHabits()
        targetHabit = habitTracker.GetHabit(habitList, int(tempHabitIdInput))
        longestStreak = habitAnalytics.GetLongestStreak(targetHabit)
        if longestStreak is not None:
            print('Longest Streak: ' + str(longestStreak) + ' days in a row')
    else:
        print('Choise could not be processed.')
        print('Listing of habit streak aborted.')
        Menu()

def MenuGetLongestStreakAllHabits():
    returnData = habitAnalytics.GetLongestStreakAllHabits()
    if returnData is not None:
        habit = returnData[1]
        longestStreak = returnData[0]
        if habit.periodicity == 'DAILY':
            print('Longest Streak on all tracked Habits is: ' + str(longestStreak) + ' days in a row')
            print('Habit: ' + str(habit.name))
            Menu()
        if habit.periodicity == 'WEEKLY':
            print('Longest Streak on all tracked Habits is: ' + str(longestStreak) + ' weeky in a row')
            print('Habit: ' + str(habit.name))
            Menu()
        else:
            print('Overall Longest Streak could not be found!')
            Menu()
    else:
        print('Overall Longest Streak could not be found!')
        Menu()

def Menu():
    print('Menu of Habit Tracker.')
    print('-----------------------')
    print('1 - Create New Habit')
    print('2 - Edit Habit')
    print('3 - Complete Habit (Mark as Done)')
    print('4 - Unpublish Habit')
    print('5 - List Tracked Habits')
    print('6 - List Habits per Periodicity')
    print('7 - GetLongestStreak of Habit')
    print('8 - GetLongestStreak of All Habits')
    print('X - Exit Program')
    
    menuChoice = input('Enter number and press ''Enter'' to run action: ')

    if menuChoice == "1":
        MenuNewHabit()
        ReturnToMenu()
    elif menuChoice == "2":
        MenuEditHabit()
        ReturnToMenu()
    elif menuChoice == "3":
        MenuMarkHabit()
        ReturnToMenu()
    elif menuChoice == "4":
        MenuUnpublishHabit()
        ReturnToMenu()
    elif menuChoice == "5":
        MenuListHabits()
        ReturnToMenu()
    elif menuChoice == "6":
        MenuListHabitsPeriodicity()
        ReturnToMenu()
    elif menuChoice == "7":
        MenuGetLongestStreakPerHabit()
        ReturnToMenu()
    elif menuChoice == "8":
        MenuGetLongestStreakAllHabits()
        ReturnToMenu()
    elif menuChoice == "X" or menuChoice == "x":
        exit()
    else:
        print('Input not found!')
        Menu()


# Run Main
if __name__ == "__main__":
    main()