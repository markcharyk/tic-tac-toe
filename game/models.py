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
        return result

    def check_for_end(self):
        """Check to see if a game is won or tied"""
        conditions = (
            set([0,3,6]),
            set([1,4,7]),
            set([2,5,8]),
            set([0,1,2]),
            set([3,4,5]),
            set([6,7,8]),
            set([0,4,8]),
            set([2,4,6]),)
        x_spaces = {i for i, turn in enumerate(self.spaces) if turn == 'X'}
        o_spaces = {i for i, turn in enumerate(self.spaces) if turn == 'O'}

        for run in conditions:
            if run.issubset(x_spaces):
                return True, 'X'
            elif run.issubset(o_spaces):
                return True, 'O'
        num_turns = len(x_spaces) + len(o_spaces)
        if num_turns == 9:
            return True, 'The cat'
        return (False,)

    def make_move(self, space, char):
        """Play one square in the game"""
        if 0 <= space < 9 and self.spaces[space] == u' ':
            self.spaces = "{0}{1}{2}".format(
                self.spaces[:space],
                char,
                self.spaces[space+1:])
        else:
            raise UnallowedError("That's an illegal move")


class UnallowedError(BaseException):
    """Exception raised when a move is not allowed"""
    pass