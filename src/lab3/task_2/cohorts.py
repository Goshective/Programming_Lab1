import os
from typing import Tuple, Set, List


VIEWS_FILENAME = "input.txt"
PATH = os.path.dirname(os.path.abspath(__file__))

class Respondent:
    def __init__(self, full_name, age):
        self.full_name = full_name
        self.age = age


class Cohorts:
    def __init__(self, cohorts):
        pass

    def add_respondent(self, respondent: Respondent):
        pass


def read_data(path):
    with open(path, 'r', encoding='utf-8') as file:
        cohorts = [int(x) for x in file.readline().rstrip().split()]
        cohorts_library = Cohorts(cohorts)
        while True:
            line = file.readline().rstrip()
            if line == "END":
                break
            full_name, age = line.split(',')
            cohorts_library.add_respondent(Respondent(full_name, age))
    return cohorts_library