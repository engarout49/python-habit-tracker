import unittest
import habitTracker
import habitAnalytics

testCaseHabitName = 'UnitTest1234'
testCaseHabitPeriodicity = 'DAILY'
testCaseHabitId = 0

class HabitTest(unittest.TestCase):
    def test_NewHabit(self):
        result = habitTracker.NewHabit(testCaseHabitName, testCaseHabitPeriodicity)
        self.assertGreater(result, 0)
        #testCaseHabitId = result
    def test_EditHabit(self):
        testHabit = habitTracker.Habit(testCaseHabitId, testCaseHabitName, testCaseHabitPeriodicity, True)
        result = testHabit.Edit('UnitTest12345', 'WEEKLY')
        self.assertTrue(result)
    def test_EditHabitBadPeriodicityDaily(self):
        testHabit = habitTracker.Habit(testCaseHabitId, testCaseHabitName, testCaseHabitPeriodicity, True)
        result = testHabit.Edit('UnitTest12345', 'daily')
        self.assertFalse(result)
    def test_EditHabitBadPeriodicityWeekly(self):
        testHabit = habitTracker.Habit(testCaseHabitId, testCaseHabitName, testCaseHabitPeriodicity, True)
        result = testHabit.Edit('UnitTest12345', 'weekly')
        self.assertFalse(result)
    def test_SyncHabits(self):
        result = habitTracker.SyncHabits()
        self.assertGreaterEqual(result.__len__(), 1)
    def test_MarkHabitDone(self):
        testHabit = habitTracker.Habit(testCaseHabitId, testCaseHabitName, testCaseHabitPeriodicity, True)
        result = testHabit.MarkDone
        self.assertTrue(result)
    def test_UnpublishHabit(self):
        testHabit = habitTracker.Habit(testCaseHabitId, testCaseHabitName, testCaseHabitPeriodicity, True)
        result = testHabit.Unpublish()
        self.assertTrue(result)
    def test_LongestStreak(self):
        testHabit = habitTracker.Habit(testCaseHabitId, testCaseHabitName, testCaseHabitPeriodicity, True)    
        result = habitAnalytics.GetLongestStreak(testHabit)
        self.assertIsNotNone(result)
    def test_ListHabitsPerPeriodicityDaily(self):
        result = habitAnalytics.ListHabitsPerPeriodicity("DAILY")
        self.assertIsNotNone(result)
    def test_ListHabitsPerPeriodicityWeekly(self):
        result = habitAnalytics.ListHabitsPerPeriodicity("WEEKLY")
        self.assertIsNotNone(result)
    def test_ListTrackedHabits(self):
        result = habitAnalytics.ListTrackedHabits()
        self.assertIsNotNone(result)

result = unittest.main()