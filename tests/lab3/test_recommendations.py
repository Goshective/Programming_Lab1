import sys
import os
import unittest

PATH = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(PATH, '..', '..')
sys.path.insert(0, src_dir)

from src.lab3.task_1.recommendations import User


class RecommendationsTestCase(unittest.TestCase):

    def test_user_common_coeff(self):
        user1 = User(1, [0, 1, 2, 2, 3])
        user2 = User(2, [4, 5, 5, 6])
        user3 = User(3, [2, 3, 4, 5, 6])

        self.assertTrue(user1.are_views_in_common(user2)[0])
        self.assertEqual(user1.are_views_in_common(user3)[1], 0.5)
        self.assertEqual(user3.are_views_in_common(user1)[1], 0.4)

    def test_user_common_views(self):
        user1 = User(1, [0, 1, 2, 2, 3])
        user2 = User(2, [4, 5, 5, 6])
        user3 = User(3, [2, 3, 4, 5, 6])

        self.assertEqual(user2.are_views_in_common(user3)[2], {4, 5, 6})
        self.assertEqual(user1.are_views_in_common(user3)[2], {2, 3})
        self.assertEqual(user3.are_views_in_common(user1)[2], {2, 3})

    def test_user_get_recommendation(self):
        user1 = User(1, [0, 1, 2, 2, 3])
        user2 = User(2, [4, 5, 5, 6])
        user3 = User(3, [2, 3, 4, 5, 6])

        self.assertEqual(user2.get_recommendation(user3.unique_views), set([]))
        self.assertEqual(user1.get_recommendation(user3.unique_views), {0, 1})
        self.assertEqual(user3.get_recommendation(user1.unique_views), {4, 5, 6})


if __name__ == "__main__":
    unittest.main()