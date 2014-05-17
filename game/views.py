from django.shortcuts import render
from django.http import HttpResponse, Http404
import json
import random
from game.models import Board, UnallowedError

def play(request):
    if request.is_ajax():
        try:
            space = int(request.POST['id'])
            board = Board.objects.get(pk=request.POST['board_id'][6:])
        except KeyError:
            return HttpResponse('Error')
        except Board.DoesNotExist:
            raise Http404("That game doesn't seem to exist")

        try:
            board.make_move(space, 'X')
        except UnallowedError:
            data = {"msg": "That's not allowed!"}
        else:
            if not board.check_for_end()[0]:
                O_space = _AI_move_random(board)
                data = {"O": O_space}
            if board.check_for_end()[0]:
                data = {"msg": ending[1]+' wins!', "end": "true"}
        return HttpResponse(
            json.dumps(data),
            content_type="application/json")
    elif request.method == 'GET':
        new_board = Board()
        new_board.save()
        return render(request, 'game/game.html', {'board_id': new_board.pk})

def _AI_move_random(board):
    """Plays an O in a random open slot"""
    blank = [i for i, j in enumerate(board.spaces) if j == ' ']
    if blank:
        move = random.choice(blank)
        board.make_move(move, 'O')
        return move
    return None
