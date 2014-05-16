from django.shortcuts import render

def play(request):
    if request.method == 'POST':
        if request.is_ajax():
            pass
    else:
        return