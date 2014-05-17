from django.shortcuts import render
from django.http import HttpResponse
import json

def play(request):
    if request.is_ajax():
        try:
            space = int(request.POST['id'])
            print space
        except KeyError:
            return HttpResponse('Error')
        return HttpResponse(json.dumps({"msg": 'You Played'}), mimetype="application/json")
    else:
        return render(request, 'game/game.html', {})