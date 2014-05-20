from django.db import models


class Board(models.Model):
    """For displaying and keeping track of the state of the game"""
    spaces = models.CharField(max_length=9, default = u'         ')
    conditions = (
        (0,3,6),
        (1,4,7),
        (2,5,8),
        (0,1,2),
        (3,4,5),
        (6,7,8),
        (0,4,8),
        (2,4,6),)

    def __repr__(self):
        result = ''
        for x in range(3):
            for space in self.spaces[x*3:(x+1)*3]:
                result = '{0}{1}   '.format(result, space)
            result = '{}\n'.format(result)
        return result

    def check_for_end(self):
        """Check to see if a game is won or tied"""
        for run in self.conditions:
            if self.spaces[run[0]] == ' ':
                continue
            if self.spaces[run[0]] == self.spaces[run[1]] and self.spaces[run[1]] == self.spaces[run[2]]:
                return True, self.spaces[run[0]]
        if ' ' not in self.spaces:
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