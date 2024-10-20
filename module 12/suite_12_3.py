import unittest
from module_12_3 import RunnerTest  # Импортируем RunnerTest
from module_12_3 import TournamentTest  # Импортируем TournamentTest

# Создаем TestSuite
suite = unittest.TestSuite()
suite.addTest(unittest.TestLoader().loadTestsFromTestCase(RunnerTest))
suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TournamentTest))

# Запускаем тесты с verbosity=2
runner = unittest.TextTestRunner(verbosity=2)
runner.run(suite)
