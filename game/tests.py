from django.test import TestCase
from game.models import Board, UnallowedError
from game.views import _AI_move_random
from django.test import Client
import json


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
        self.assertEqual(returned_tup[1], 'The cat')

    def test_Xs_turn(self):
        self.b.spaces = u'XX  O O  '
        returned_tup = self.b.check_for_end()
        self.assertFalse(returned_tup[0])

    def test_Os_turn(self):
        self.b.spaces = u'XX    O  '
        returned_tup = self.b.check_for_end()
        self.assertFalse(returned_tup[0])

    def test_start_of_game(self):
        self.b.spaces = u'         '
        returned_tup = self.b.check_for_end()
        self.assertFalse(returned_tup[0])


class ViewsTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_new_game(self):
        resp = self.client.get('/play/')
        self.assertEquals(resp.status_code, 200)
        self.assertContains(resp, "<div id='board-")
        self.assertContains(resp, 'onclick="makeMove(')

    def test_AI_move_full(self):
        """Tests the AI trying to move on a full board"""
        b = Board()
        b.spaces = 'XXOOOXXOX'
        self.assertIsNone(_AI_move_random(b))

    def test_AI_move_empty(self):
        """Tests the AI placing a move on an empty board"""
        b = Board()
        b.spaces = '         '
        self.assertIn(_AI_move_random(b), range(9))

    def test_AI_move_middle_of_game(self):
        """Tests the AI placing a move on a partially-filled board"""
        b = Board()
        b.spaces = 'XXO X  O '
        self.assertIn(_AI_move_random(b), [3, 5, 6, 8])