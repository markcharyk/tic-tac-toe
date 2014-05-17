from django.shortcuts import render
from django.http import HttpResponse, Http404
import json

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
        return HttpResponse(
            json.dumps({"msg": 'You Played'}),
            content_type="application/json")
    else:
        new_board = Board()
        new_board.save()
        return render(request, 'game/game.html', {'board_id': new_board.pk})