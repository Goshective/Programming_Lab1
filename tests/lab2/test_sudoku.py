import sys
import os
import unittest

current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, '..', '..')
sys.path.insert(0, src_dir)

from src.lab2.sudoku import (
    read_sudoku, 
    group, 
    get_row, 
    get_col, 
    get_block, 
    find_empty_positions,
    find_possible_values,
    solve,
    check_solution,
    generate_sudoku
)


class SudokuTestCase(unittest.TestCase):

    def test_group(self):
        self.assertEqual(group([1], 1), [[1]])
        self.assertEqual(group([1,2,3,4], 2), [[1, 2], [3, 4]])
        self.assertEqual(group([1,2,3,4,5,6,7,8,9], 3), [[1, 2, 3], [4, 5, 6], [7, 8, 9]])

    def test_get_row(self):
        self.assertEqual(get_row([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0)), ['1', '2', '.'])
        self.assertEqual(get_row([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (1, 0)), ['4', '.', '6'])
        self.assertEqual(get_row([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (2, 0)), ['.', '8', '9'])

    def test_get_col(self):
        self.assertEqual(get_col([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0)), ['1', '4', '7'])
        self.assertEqual(get_col([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (0, 1)), ['2', '.', '8'])
        self.assertEqual(get_col([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (0, 2)), ['3', '6', '9'])

    def test_get_block(self):
        grid = read_sudoku('src/lab2/puzzle1.txt')
        
        self.assertEqual(get_block(grid, (0, 1)), ['5', '3', '.', '6', '.', '.', '.', '9', '8'])
        self.assertEqual(get_block(grid, (4, 7)), ['.', '.', '3', '.', '.', '1', '.', '.', '6'])
        self.assertEqual(get_block(grid, (8, 8)), ['2', '8', '.', '.', '.', '5', '.', '7', '9'])

    def test_find_empty(self):
        self.assertEqual(find_empty_positions([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']]), (0, 2))
        self.assertEqual(find_empty_positions([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']]), (1, 1))
        self.assertEqual(find_empty_positions([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']]), (2, 0))

    def test_find_possible(self):
        grid = read_sudoku('src/lab2/puzzle1.txt')

        self.assertEqual(find_possible_values(grid, (0,2)), {'1', '2', '4'})
        self.assertEqual(find_possible_values(grid, (4,7)), {'2', '5', '9'})

    def test_solve(self):
        grid = read_sudoku('src/lab2/puzzle1.txt')

        self.assertEqual(solve(grid), 
                         [['5', '3', '4', '6', '7', '8', '9', '1', '2'], ['6', '7', '2', '1', '9', '5', '3', '4', '8'], ['1', '9', '8', '3', '4', '2', '5', '6', '7'], ['8', '5', '9', '7', '6', '1', '4', '2', '3'], ['4', '2', '6', '8', '5', '3', '7', '9', '1'], ['7', '1', '3', '9', '2', '4', '8', '5', '6'], ['9', '6', '1', '5', '3', '7', '2', '8', '4'], ['2', '8', '7', '4', '1', '9', '6', '3', '5'], ['3', '4', '5', '2', '8', '6', '1', '7', '9']]
                         )
    
    def test_check_solution(self):
        grid = [['5', '3', '4', '6', '7', '8', '9', '1', '2'], ['6', '7', '2', '1', '9', '5', '3', '4', '8'], ['1', '9', '8', '3', '4', '2', '5', '6', '7'], ['8', '5', '9', '7', '6', '1', '4', '2', '3'], ['4', '2', '6', '8', '5', '3', '7', '9', '1'], ['7', '1', '3', '9', '2', '4', '8', '5', '6'], ['9', '6', '1', '5', '3', '7', '2', '8', '4'], ['2', '8', '7', '4', '1', '9', '6', '3', '5'], ['3', '4', '5', '2', '8', '6', '1', '7', '9']]
        
        self.assertTrue(check_solution(grid))

        grid[0][0] = '6'
        self.assertFalse(check_solution(grid))

        grid[0][0] = '5'
        grid[4][4] = '6'
        self.assertFalse(check_solution(grid))

    def test_generate_sudoku(self):
        grid = generate_sudoku(40)
        self.assertEqual(sum(1 for row in grid for e in row if e == '.'), 41)
        solution = solve(grid)
        self.assertTrue(check_solution(solution))

        grid = generate_sudoku(1000)
        self.assertEqual(sum(1 for row in grid for e in row if e == '.'), 0)
        solution = solve(grid)
        self.assertTrue(check_solution(solution))

        grid = generate_sudoku(0)
        self.assertEqual(sum(1 for row in grid for e in row if e == '.'), 81)
        solution = solve(grid)
        self.assertTrue(check_solution(solution))


if __name__ == "__main__":
    unittest.main()