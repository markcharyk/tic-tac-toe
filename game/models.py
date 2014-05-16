from django.db import models

class Board(models.Model):
    """For displaying and keeping track of the state of the game"""
    spaces = models.CharField(max_length=9)

    def __repr__(self):
        result = ''
        for x in range(3):
            for space in self.spaces[x*3:(x+1)*3]:
                result = '%s%s   ' % (result, space)
            result = '%s\n' % result
        return result

    def check_for_end(self):
        conditions = (
            set([0,3,6]),
            set([1,4,6]),
            set([2,5,8]),
            set([0,1,2]),
            set([3,4,5]),
            set([6,7,8]),
            set([0,4,8]),
            set([2,4,6]),
        )

        x_spaces = {i for i, turn in enumerate(self.spaces) if turn == 'X'}
        o_spaces = {i for i, turn in enumerate(self.spaces) if turn == 'O'}

        for run in conditions:
            if run.issubset(x_spaces):
                return True, 'X'
            elif run.issubset(o_spaces):
                return True, 'O'
        return False