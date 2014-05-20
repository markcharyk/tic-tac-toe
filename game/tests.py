from django.test import TestCase
from game.models import Board, UnallowedError
from game.views import _AI_move_random
from django.test import Client, LiveServerTestCase
from selenium import webdriver
from django.core.urlresolvers import reverse
import json
import os
from time import sleep


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
        """Test that a new game being loaded loads the board correctly"""
        resp = self.client.get('/play/')
        self.assertEquals(resp.status_code, 200)
        self.assertContains(resp, "<div id='board-")
        self.assertContains(resp, 'onclick="makeMove(')

    def test_AI_move_full(self):
        """Test the AI trying to move on a full board"""
        b = Board()
        b.spaces = 'XXOOOXXOX'
        self.assertIsNone(_AI_move_random(b))

    def test_AI_move_empty(self):
        """Test the AI placing a move on an empty board"""
        b = Board()
        b.spaces = '         '
        self.assertIn(_AI_move_random(b), range(9))

    def test_AI_move_middle_of_game(self):
        """Test the AI placing a move on a partially-filled board"""
        b = Board()
        b.spaces = 'XXO X  O '
        self.assertIn(_AI_move_random(b), [3, 5, 6, 8])


class BrowserTest(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        cls.selenium = webdriver.Chrome()
        super(BrowserTest, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(BrowserTest, cls).tearDownClass()

    def test_X_move(self):
        """Test that a move unsets the given canvas's onclick attr"""
        self.selenium.get('{0}{1}'.format(self.live_server_url, reverse('play')))
        canv = self.selenium.find_element_by_id('space-0')
        canv.click()
        sleep(2)
        self.assertEqual(canv.get_attribute('onclick'), '')

    def test_end_game(self):
        """Test that the final play unsets all canvases' onclick attrs"""
        self.selenium.get('{0}{1}'.format(self.live_server_url, reverse('play')))
        b = self.selenium.find_element_by_class_name('game-board')
        board = Board.objects.get(pk=int(b.get_attribute('id')[6:]))
        board.spaces = 'OXOOXXXO '
        board.save()
        canv = self.selenium.find_element_by_id('space-8')
        canv.click()
        sleep(2)
        alert = self.selenium.switch_to.alert
        alert.accept()
        for i in range(9):
            self.assertEqual(self.selenium.find_element_by_id('space-'+str(i)).get_attribute('onclick'), '')

    def test_move_ajax(self):
        """Test that the clicked move and comptuer move are posted to the board in the database"""
        self.selenium.get('{0}{1}'.format(self.live_server_url, reverse('play')))
        canv = self.selenium.find_element_by_id('space-0')
        canv.click()
        sleep(1)
        b = self.selenium.find_element_by_class_name('game-board')
        board = Board.objects.get(pk=int(b.get_attribute('id')[6:]))
        self.assertEqual('X', board.spaces[0])
        self.assertIn('O', board.spaces)

    def test_X_wins(self):
        """Test for X winning condition
        Note, the moves won't be shown on the test browser"""
        self.selenium.get('{0}{1}'.format(self.live_server_url, reverse('play')))
        b = self.selenium.find_element_by_class_name('game-board')
        board = Board.objects.get(pk=int(b.get_attribute('id')[6:]))
        board.spaces = 'X O XO   '
        board.save()
        canv = self.selenium.find_element_by_id('space-8')
        canv.click()
        sleep(1)
        alert = self.selenium.switch_to.alert
        self.assertIn("X wins!", alert.text)
        alert.accept()

    def test_O_wins(self):
        """Test for O winning condition
        Note that the moves won't be shown on the test browser"""
        self.selenium.get('{0}{1}'.format(self.live_server_url, reverse('play')))
        b = self.selenium.find_element_by_class_name('game-board')
        board = Board.objects.get(pk=int(b.get_attribute('id')[6:]))
        # Set up the board so no matter what move O makes it is a win
        board.spaces = 'O OOXX X '
        board.save()
        canv = self.selenium.find_element_by_id('space-8')
        canv.click()
        sleep(1)
        alert = self.selenium.switch_to.alert
        self.assertIn("O wins!", alert.text)
        alert.accept()

    def test_cats_game(self):
        """Test for tie game condition
        Note that the moves won't be shown on the test browser"""
        self.selenium.get('{0}{1}'.format(self.live_server_url, reverse('play')))
        b = self.selenium.find_element_by_class_name('game-board')
        board = Board.objects.get(pk=int(b.get_attribute('id')[6:]))
        board.spaces = 'OXOOXXXO '
        board.save()
        canv = self.selenium.find_element_by_id('space-8')
        canv.click()
        sleep(1)
        alert = self.selenium.switch_to.alert
        self.assertIn("The cat wins!", alert.text)
        alert.accept()

    def test_re_click(self):
        """Test that a click on an occupied space has no effect"""
        self.selenium.get('{0}{1}'.format(self.live_server_url, reverse('play')))
        canv = self.selenium.find_element_by_id('space-0')
        canv.click()
        sleep(2)
        tx = canv.text
        canv.click()
        sleep(2)
        self.assertEqual(tx, canv.text)
