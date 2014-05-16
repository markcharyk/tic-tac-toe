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
