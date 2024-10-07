import sys
import os
import unittest

current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, '..', '..')
sys.path.insert(0, src_dir)

from src.lab3.sudoku import group


class SudokuTestCase(unittest.TestCase):

    def test_group(self):
        self.assertEqual(group([1], 1), [[1]])
        self.assertEqual(group([1,2,3,4], 2), [[1, 2], [3, 4]])
        self.assertEqual(group([1,2,3,4,5,6,7,8,9], 3), [[1, 2, 3], [4, 5, 6], [7, 8, 9]])

if __name__ == "__main__":
    unittest.main()