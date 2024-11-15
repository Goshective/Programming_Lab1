import os
import sys
from typing import Tuple, Set, List
from bisect import bisect_left


INPUT_FILENAME = "input.txt"
PATH = os.path.dirname(os.path.abspath(__file__))


class Respondent:
    def __init__(self, full_name, age):
        self.full_name = full_name
        self.age = age

    def __lt__(self, obj: 'Respondent'):
        if self.age > obj.age: return True
        return self.full_name < obj.full_name
    
    def __str__(self):
        return f'{self.full_name} ({self.age})'


class Cohorts:
    def __init__(self, cohorts: list[str]):
        self.cohorts = [0] + cohorts
        self.distribution = {age: [] for age in cohorts}
        self.distribution[0] = []

    def add_respondent(self, respondent: Respondent):
        if respondent.age < 0 or respondent.age > 123:
            return
        idx = bisect_left(self.cohorts, respondent.age)
        if idx == len(self.cohorts):
            key = self.cohorts[-1]
        else:
            key = self.cohorts[idx-1]
        self.distribution[key].append(respondent)

    def print(self):
        age_ranges = self.cohorts[::-1]
        
        for i, age in enumerate(age_ranges):
            respondents = [respondent for respondent in self.distribution[age]]
            if not len(respondents):
                continue

            if i == 0:
                group_name = f'{age+1}+'
            else:
                str_age = age + 1 if age != 0 else age
                group_name = f'{str_age}-{age_ranges[i-1]}'

            print(group_name + ':', end=' ')
            respondents.sort()
            print(*respondents, sep=', ')
            print()
            

def parse_args(*args):
    res = []
    for i in range(1, len(args)):
        arg = args[i]
        if i.isnumeric():
            res.append(int(arg))
        else:
            return None
    return res

def read_data(path, args=None):
    with open(path, 'r', encoding='utf-8') as file:
        if args is None:
            cohorts = [int(x) for x in file.readline().rstrip().split()]
        else:
            file.readline()
            cohorts = args
        cohorts_library = Cohorts(cohorts)
        while True:
            line = file.readline().rstrip()
            if line == "END":
                break
            full_name, age = line.split(', ')
            cohorts_library.add_respondent(Respondent(full_name, int(age)))
    return cohorts_library

if __name__ == '__main__':
    args = parse_args(sys.argv)
    if args is None:
        print("Некорректные аргументы")
        exit(0)
    people_by_cohorts = read_data(os.path.join(PATH, INPUT_FILENAME))

    # print(people_by_cohorts.distribution)

    people_by_cohorts.print()