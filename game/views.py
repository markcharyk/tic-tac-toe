from django.shortcuts import render
from django.http import HttpResponse, Http404
import json
import random
from game.models import Board

def play(request):
    if request.is_ajax():
        try:
            space = int(request.POST['id'])
            board = Board.objects.get(pk=request.POST['board_id'][6:])
        except KeyError:
            return HttpResponse('Error')
        except Board.DoesNotExist:
            raise Http404("That game doesn't seem to exist")

        board.make_move(space, 'X')
        ending = board.check_for_end()
        if ending[0]:
            if ending[1] == 'C':
                return HttpResponse(
                    json.dumps({"msg": "Cat's game!"}),
                    content_type="application/json")
            return HttpResponse(
                json.dumps({"msg": ending[1]+' wins!'}),
                content_type="application/json")
        O_space = _AI_move_random(board)
        return HttpResponse(
            json.dumps({"msg": 'You Played', "O": O_space}),
            content_type="application/json")
    elif request.method == 'GET':
        new_board = Board()
        new_board.save()
        return render(request, 'game/game.html', {'board_id': new_board.pk})

def _AI_move_random(board):
    """Plays an O in a random open slot"""
    blank = [i for i, j in enumerate(board.spaces) if j == ' ']
    move = random.choice(blank)
    board.make_move(move, 'O')
    return move