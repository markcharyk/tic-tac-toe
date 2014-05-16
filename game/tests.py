from django.test import TestCase
from game.models import Board, UnallowedError


class MakeMoveTest(TestCase):
    def setUp(self):
        self.b = Board()

    def test_X_move(self):
        self.b.make_move(0, 'X')
        self.assertEqual(self.b.spaces, u'X        ')

    def test_O_move(self):
        self.b.spaces = u'X        '
        self.b.make_move(4, 'O')
        self.assertEqual(self.b.spaces, u'X   O    ')

    def test_off_board_move(self):
        with self.assertRaises(UnallowedError):
            self.b.make_move(10, 'X')

    def test_filled_space(self):
        self.b.spaces = u'    X    '
        with self.assertRaises(UnallowedError):
            self.b.make_move(4, 'O')


class CheckForEndTest(TestCase):
    def setUp(self):
        self.b = Board()

    def test_X_wins(self):
        self.b.spaces = u'X O XO  X'
        returned_tup = self.b.check_for_end()
        self.assertTrue(returned_tup[0])
        self.assertEqual(returned_tup[1], 'X')

    def test_O_wins(self):
        self.b.spaces = u'OOOX XX  '
        returned_tup = self.b.check_for_end()
        self.assertTrue(returned_tup[0])
        self.assertEqual(returned_tup[1], 'O')

    def test_cats_game(self):
        self.b.spaces = u'OXOOXXXOX'
        returned_tup = self.b.check_for_end()
        self.assertTrue(returned_tup[0])
        self.assertEqual(returned_tup[1], 'C')

    def test_Xs_turn(self):
        self.b.spaces = u'XX  O O  '
        returned_tup = self.b.check_for_end()
        self.assertFalse(returned_tup[0])
        self.assertEqual(returned_tup[1], 'X')

    def test_Os_turn(self):
        self.b.spaces = u'XX    O  '
        returned_tup = self.b.check_for_end()
        self.assertFalse(returned_tup[0])
        self.assertEqual(returned_tup[1], 'O')

    def test_start_of_game(self):
        self.b.spaces = u'         '
        returned_tup = self.b.check_for_end()
        self.assertFalse(returned_tup[0])
        self.assertEqual(returned_tup[1], 'X')