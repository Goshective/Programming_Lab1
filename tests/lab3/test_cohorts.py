import sys
import os
import unittest

PATH = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(PATH, '..', '..')
sys.path.insert(0, src_dir)

from src.lab3.task_2.cohorts import (
    Cohorts,
    Respondent,
    parse_args,
    read_data_file
)


class CohortsTestCase(unittest.TestCase):

    def test_args_parsing(self):
        self.assertEqual(parse_args(
            ['cohorts.py', '18', '25', '35', '45', '60', '80', '100']), 
            [18, 25, 35, 45, 60, 80, 100])
        self.assertEqual(parse_args(
            ['task_2/cohorts.py', '18', '25', '35', '45', '60', '80', '100']), 
            [18, 25, 35, 45, 60, 80, 100])
        
        self.assertIsNone(parse_args(
            ['cohorts.py', '18', '25', 'Thirty five', '45']))
        self.assertIsNone(parse_args(
            ['cohorts.py', '18', '25.5', '35', '45']))
        self.assertIsNone(parse_args(
            ['cohorts.py', '18', '10', '9', '7']))

    def test_add_respondent_wrong_age(self):
        dist = [18, 25, 35, 45, 60, 80, 100]
        cohorts = Cohorts(dist)

        respondent1 = Respondent('A A A', 124)
        cohorts.add_respondent(respondent1)

        self.assertEqual(cohorts.distribution, {key: [] for key in [0] + dist})

    def test_add_respondent_age_borders(self):
        dist = [18, 25, 35, 45, 60, 80, 100]
        cohorts = Cohorts(dist)

        respondent1 = Respondent('A A A', 123)
        respondent2 = Respondent('A A A', 0)
        cohorts.add_respondent(respondent1)
        cohorts.add_respondent(respondent2)

        self.assertEqual(cohorts.get_cohort(0), [respondent2])
        self.assertEqual(cohorts.get_cohort(100), [respondent1])

    def test_add_respondent_cohorts_borders(self):
        dist = [18, 25, 35, 45, 60, 80, 100]
        cohorts = Cohorts(dist)

        resp1 = Respondent('A A A', 25)
        resp2 = Respondent('A A B', 26)
        resp3 = Respondent('A A C', 35)
        resp4 = Respondent('A A D', 36)
        for resp in (resp1, resp2, resp3, resp4):
            cohorts.add_respondent(resp)
        ages = [[r.age for r in cohorts.get_cohort(key)] for key in (18, 25, 35)]

        self.assertEqual(ages, [[25], [26, 35], [36]])

    def test_sort_cohort(self):
        dist = [18, 25, 35, 45, 60, 80, 100]
        cohorts = Cohorts(dist)

        resp1 = Respondent('A A B', 26)
        resp2 = Respondent('A A A', 26)
        resp3 = Respondent('A A C', 30)
        resp4 = Respondent('A A D', 35)
        for resp in (resp1, resp2, resp3, resp4):
            cohorts.add_respondent(resp)
        respondents = [resp for resp in cohorts.distribution[25]]
        respondents.sort()
        names = [r.full_name for r in respondents]

        self.assertEqual(names, ['A A D', 'A A C', 'A A A', 'A A B'])

    def test_reading_data(self):
        input_path = os.path.join(PATH, 'test_input.txt')
        data = [
            '18 25 35 45 60 80 100\n',
            'A A A, 18\n',
            'A A B, 8\n',
            'A A C, 19\n',
            'END']
        with open(input_path, 'w') as f:
            f.writelines(data)
        distribution = [0, 18, 25, 35, 45, 60, 80, 100]
        cohorts = read_data_file(input_path)

        self.assertEqual(cohorts.cohorts, distribution)
        resp_by_age = []
        for age in distribution[:3]:
            respondents = [respondent.age for respondent in cohorts.get_cohort(age)]
            resp_by_age.append(respondents)
        
        self.assertEqual(resp_by_age, [[18, 8], [19], []])


if __name__ == "__main__":
    unittest.main()