import os
import sys
from typing import Tuple, Set, List
from bisect import bisect_left


INPUT_FILENAME = "input.txt"
OUTPUT_FILENAME = "output.txt"
PATH = os.path.dirname(os.path.abspath(__file__))


class Respondent:
    def __init__(self, full_name: str, age: int):
        self.full_name = full_name
        self.age = age

    def __lt__(self, obj: 'Respondent') -> bool:
        if self.age > obj.age: return True
        return self.full_name < obj.full_name
    
    def __str__(self) -> str:
        return f'{self.full_name} ({self.age})'


class Cohorts:
    def __init__(self, cohorts: list[str]):
        self.cohorts = [0] + cohorts
        self.distribution = {age: [] for age in cohorts}
        self.distribution[0] = []

    def add_respondent(self, respondent: Respondent) -> None:
        if respondent.age < 0 or respondent.age > 123:
            return

        idx = bisect_left(self.cohorts, respondent.age)

        if respondent.age == 0:
            key = self.cohorts[0]
        elif idx == len(self.cohorts):
            key = self.cohorts[-1]
        else:
            key = self.cohorts[idx-1]
        self.distribution[key].append(respondent)

    def print(self, output_file=None) -> None:
        age_ranges = self.cohorts[::-1]
        if output_file is None:
            print()
        for i, age in enumerate(age_ranges):
            respondents = [respondent for respondent in self.distribution[age]]
            if not len(respondents):
                continue

            if i == 0:
                group_name = f'{age+1}+'
            else:
                str_age = age + 1 if age != 0 else age
                group_name = f'{str_age}-{age_ranges[i-1]}'

            respondents.sort()

            print(group_name + ':', end=' ', file=output_file)
            print(*respondents, sep=', ', file=output_file)
            print(file=output_file)

def parse_args(args):
    res = []
    for i in range(1, len(args)):
        arg = args[i]
        if arg.isnumeric():
            res.append(int(arg))
        else:
            return None
    return res


def read_data_file(path):
    with open(path, 'r', encoding='utf-8') as file:
        cohorts = [int(x) for x in file.readline().rstrip().split()]

        cohorts_library = Cohorts(cohorts)
        while True:
            line = file.readline().rstrip()
            if line == "END":
                break
            full_name, age = line.split(', ')
            cohorts_library.add_respondent(Respondent(full_name, int(age)))
    return cohorts_library


def read_data_args(args):
    cohorts = args
    cohorts_library = Cohorts(cohorts)
    while True:
        line = input()
        if line == "END":
            break
        full_name, age = line.split(', ')
        cohorts_library.add_respondent(Respondent(full_name, int(age)))
    return cohorts_library


def main():
    args = sys.argv
    is_command = args[0] == "cohorts.py"
    parsed_args = parse_args(args)
    if args is None:
        print("Некорректные аргументы")
        exit(0)

    if is_command:
        people_by_cohorts = read_data_args(parsed_args)
        people_by_cohorts.print()
        pass
    else:
        people_by_cohorts = read_data_file(os.path.join(PATH, INPUT_FILENAME))
        with open(os.path.join(PATH, OUTPUT_FILENAME), 'w', encoding='utf-8') as output_file:
            people_by_cohorts.print(output_file=output_file)


if __name__ == '__main__':
    main()