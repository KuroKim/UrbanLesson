
import unittest


# Декоратор для проверки значения атрибута is_frozen
def skip_if_frozen(func):
    def wrapper(self, *args, **kwargs):
        if self.is_frozen:
            self.skipTest('Тесты в этом кейсе заморожены')
        else:
            return func(self, *args, **kwargs)
    return wrapper


class Runner:
    def __init__(self, name, speed=5):
        self.name = name
        self.distance = 0
        self.speed = speed

    def run(self):
        self.distance += self.speed * 2

    def walk(self):
        self.distance += self.speed

    def __str__(self):
        return self.name

    def __eq__(self, other):
        if isinstance(other, str):
            return self.name == other
        elif isinstance(other, Runner):
            return self.name == other.name


class RunnerTest(unittest.TestCase):
    is_frozen = False

    @skip_if_frozen
    def test_walk(self):
        runner = Runner('Test Runner')
        for _ in range(10):
            runner.walk()
        self.assertEqual(runner.distance, 50)

    @skip_if_frozen
    def test_run(self):
        runner = Runner('Test Runner')
        for _ in range(10):
            runner.run()
        self.assertEqual(runner.distance, 100)

    @skip_if_frozen
    def test_challenge(self):
        runner1 = Runner('Runner 1')
        runner2 = Runner('Runner 2')
        for _ in range(10):
            runner1.run()
            runner2.walk()
        self.assertNotEqual(runner1.distance, runner2.distance)


class Tournament:
    def __init__(self, distance, *participants):
        self.full_distance = distance
        self.participants = list(participants)

    def start(self):
        finishers = {}
        place = 1
        while self.participants:
            for participant in self.participants:
                participant.run()
                if participant.distance >= self.full_distance:
                    finishers[place] = participant
                    place += 1
                    self.participants.remove(participant)

        return finishers


class TournamentTest(unittest.TestCase):
    is_frozen = True  # Заморожено, тесты будут пропущены

    @classmethod
    def setUpClass(cls):
        cls.all_results = {}

    def setUp(self):
        self.runner1 = Runner('Усэйн', 10)
        self.runner2 = Runner('Андрей', 9)
        self.runner3 = Runner('Ник', 3)

    @classmethod
    def tearDownClass(cls):
        for result_id, result in cls.all_results.items():
            print(f"Результат: {', '.join([str(runner) for runner in result.values()])}")

    @skip_if_frozen
    def test_usain_and_nick(self):
        tournament = Tournament(90, self.runner1, self.runner3)
        result = tournament.start()
        self.__class__.all_results[id(result)] = result
        self.assertTrue(result[max(result.keys())] == self.runner3)

    @skip_if_frozen
    def test_andrey_and_nick(self):
        tournament = Tournament(90, self.runner2, self.runner3)
        result = tournament.start()
        self.__class__.all_results[id(result)] = result
        self.assertTrue(result[max(result.keys())] == self.runner3)

    @skip_if_frozen
    def test_usain_andrey_and_nick(self):
        tournament = Tournament(90, self.runner1, self.runner2, self.runner3)
        result = tournament.start()
        self.__class__.all_results[id(result)] = result
        self.assertTrue(result[max(result.keys())] == self.runner3)


if __name__ == '__main__':
    unittest.main()