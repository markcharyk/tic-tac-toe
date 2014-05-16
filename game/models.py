from django.db import models

class Board(models.Model):
    """For displaying and keeping track of the state of the game"""
    spaces = models.CharField(max_length=9, default = u'         ')

    def __repr__(self):
        result = ''
        for x in range(3):
            for space in self.spaces[x*3:(x+1)*3]:
                result = '{0}{1}   '.format(result, space)
            result = '{}\n'.format(result)
        return result.trim()

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
        if len(x_spaces) + len(o_spaces) == 9:
            return True, 'C'
        return False

    def make_move(self, space, char):
        import pdb; pdb.set_trace()
        if 0 <= space < 9 and self.spaces[space] == u' ':
            self.spaces = "{0}{1}{2}".format(self.spaces[:space], char, self.spaces[space+1:])
        else:
            raise UnallowedError("That's an illegal move")


class UnallowedError(BaseException):
    """Exception raised when a move is not allowed"""
    pass