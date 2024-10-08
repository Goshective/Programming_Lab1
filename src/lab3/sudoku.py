import os
import pathlib
import typing as tp
import multiprocessing

from random import choice, randint
import time

T = tp.TypeVar("T")


def read_sudoku(path: tp.Union[str, pathlib.Path]) -> tp.List[tp.List[str]]:
    """ Прочитать Судоку из указанного файла """
    path = pathlib.Path(path)
    with path.open() as f:
        puzzle = f.read()
    return create_grid(puzzle)


def create_grid(puzzle: str) -> tp.List[tp.List[str]]:
    digits = [c for c in puzzle if c in "123456789."]
    grid = group(digits, 9)
    return grid


def display(grid: tp.List[tp.List[str]]) -> None:
    """Вывод Судоку """
    width = 2
    line = "+".join(["-" * (width * 3)] * 3)
    for row in range(9):
        print(
            "".join(
                grid[row][col].center(width) + ("|" if str(col) in "25" else "") for col in range(9)
            )
        )
        if str(row) in "25":
            print(line)
    print()


def group(values: tp.List[T], n: int) -> tp.List[tp.List[T]]:
    """
    Сгруппировать значения values в список, состоящий из списков по n элементов
    >>> group([1,2,3,4], 2)
    [[1, 2], [3, 4]]
    >>> group([1,2,3,4,5,6,7,8,9], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    res = [[values[n * i + j] for j in range(n)] for i in range(n)]
    return res


def get_row(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения для номера строки, указанной в pos
    >>> get_row([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '2', '.']
    >>> get_row([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (1, 0))
    ['4', '.', '6']
    >>> get_row([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (2, 0))
    ['.', '8', '9']
    """
    return grid[pos[0]]


def get_col(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения для номера столбца, указанного в pos
    >>> get_col([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '4', '7']
    >>> get_col([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (0, 1))
    ['2', '.', '8']
    >>> get_col([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (0, 2))
    ['3', '6', '9']
    """
    return [grid[i][pos[1]] for i in range(len(grid))]


def get_block(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения из квадрата, в который попадает позиция pos
    >>> grid = read_sudoku('puzzle1.txt')
    >>> get_block(grid, (0, 1))
    ['5', '3', '.', '6', '.', '.', '.', '9', '8']
    >>> get_block(grid, (4, 7))
    ['.', '.', '3', '.', '.', '1', '.', '.', '6']
    >>> get_block(grid, (8, 8))
    ['2', '8', '.', '.', '.', '5', '.', '7', '9']
    """
    block_cords = 3 * (pos[0] // 3), 3 * (pos[1] // 3)
    return [grid[block_cords[0] + i // 3][block_cords[1] + i % 3] for i in range(9)]


def find_empty_positions(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.Tuple[int, int]]:
    """Найти первую свободную позицию в пазле
    >>> find_empty_positions([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']])
    (0, 2)
    >>> find_empty_positions([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']])
    (1, 1)
    >>> find_empty_positions([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']])
    (2, 0)
    """
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == '.':
                return (i, j)
    return (len(grid), len(grid[0]))


def find_possible_values(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.Set[str]:
    """Вернуть множество возможных значения для указанной позиции
    >>> grid = read_sudoku('puzzle1.txt')
    >>> values = find_possible_values(grid, (0,2))
    >>> values == {'1', '2', '4'}
    True
    >>> values = find_possible_values(grid, (4,7))
    >>> values == {'2', '5', '9'}
    True
    """
    all_values = set('123456789')
    row_values = set([v for v in get_row(grid, pos) if v != '.'])
    col_values = set([v for v in get_col(grid, pos) if v != '.'])
    block_values = set([v for v in get_block(grid, pos) if v != '.'])

    possible_row = all_values - row_values
    possible_col = all_values - col_values
    possible_block = all_values - block_values

    return possible_row & possible_col & possible_block




def solve(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.List[tp.List[str]]]:
    """ Решение пазла, заданного в grid """
    """ Как решать Судоку?
        1. Найти свободную позицию
        2. Найти все возможные значения, которые могут находиться на этой позиции
        3. Для каждого возможного значения:
            3.1. Поместить это значение на эту позицию
            3.2. Продолжить решать оставшуюся часть пазла
    >>> grid = read_sudoku('puzzle1.txt')
    >>> solve(grid)
    [['5', '3', '4', '6', '7', '8', '9', '1', '2'], ['6', '7', '2', '1', '9', '5', '3', '4', '8'], ['1', '9', '8', '3', '4', '2', '5', '6', '7'], ['8', '5', '9', '7', '6', '1', '4', '2', '3'], ['4', '2', '6', '8', '5', '3', '7', '9', '1'], ['7', '1', '3', '9', '2', '4', '8', '5', '6'], ['9', '6', '1', '5', '3', '7', '2', '8', '4'], ['2', '8', '7', '4', '1', '9', '6', '3', '5'], ['3', '4', '5', '2', '8', '6', '1', '7', '9']]
    """
    pos = find_empty_positions(grid)
    if pos == (len(grid), len(grid)):
        return grid
    
    possible_values = find_possible_values(grid, pos)
    for v in possible_values:
        grid_copy = [row.copy() for row in grid]
        grid_copy[pos[0]][pos[1]] = v
        res = solve(grid_copy)
        if res:
            return res
    
    return []        


def check_solution(solution: tp.List[tp.List[str]]) -> bool:
    """ Если решение solution верно, то вернуть True, в противном случае False 
    >>> grid = read_sudoku('puzzle1.txt')
    >>> check_solution(solve(grid))
    True
    >>> grid = read_sudoku('puzzle1.txt')
    >>> grid[0][0] = '6'
    >>> check_solution(solve(grid))
    False
    """

    all_values = set('123456789')

    for i in range(9):
        row = set(get_row(solution, (i, 0)))
        col = set(get_col(solution, (0, i)))
        block = set(get_block(solution, (3 * (i // 3), 3 * (i % 3))))
        if not (row == all_values and col == all_values and block == all_values):
            return False
    
    return True


def generate_sudoku(N: int) -> tp.List[tp.List[str]]:
    """Генерация судоку заполненного на N элементов
    >>> grid = generate_sudoku(40)
    >>> sum(1 for row in grid for e in row if e == '.')
    41
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(1000)
    >>> sum(1 for row in grid for e in row if e == '.')
    0
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(0)
    >>> sum(1 for row in grid for e in row if e == '.')
    81
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    """
    while True:
        grid = [['.' for _ in range(9)] for _ in range(9)]
        rand_set = set('123456789')
        for i in range(9):
            grid[i][randint(0, 8)] = rand_set.pop()
        for i in range(3 * 9):
            while True:
                idx = choice(list(range(81)))
                y, x = idx // 9, idx % 9
                if grid[y][x] != ".":
                    continue
                values = find_possible_values(grid, (y, x))
                if not values:
                    continue
                grid[y][x] = values.pop()
                break


        fin_grid = solve(grid)
        if fin_grid:
            break
    
    del_lst = list(range(81))
    for _ in range(min(81, 81 - N)):
        idx = choice(del_lst)
        del_lst.remove(idx)
        fin_grid[idx // 9][idx % 9] = "."
    
    return fin_grid


def run_solve(filename: str) -> None:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    grid = read_sudoku(os.path.join(current_dir, filename))

    # display(grid)

    start = time.time()
    solution = solve(grid)
    end = time.time()
    if not solution:
        print(f"Puzzle {filename} can't be solved")
    else:
        if check_solution(solution):
            # display(solution)
            print('...')
        else:
            print('Solution is not correct.')
    print(f"{filename}: {end-start}")

def run_multiprocess():
    for filename in ("puzzle1.txt", "puzzle2.txt", "puzzle3.txt"):
        p = multiprocessing.Process(target=run_solve, args=(filename,))
        p.start()

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    for filename in ("puzzle1.txt", "puzzle2.txt", "puzzle3.txt"):
        grid = read_sudoku(os.path.join(current_dir, filename))

        display(grid)

        start = time.time()
        solution = solve(grid)
        end = time.time()
        if not solution:
            print(f"Puzzle {filename} can't be solved")
        else:
            if check_solution(solution):
                print(f"{filename}: {round(end-start, 5)} s")
                print('...')
                display(solution)
            else:
                print('Solution is not correct.')

    display(generate_sudoku(40))