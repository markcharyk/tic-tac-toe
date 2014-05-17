from django.contrib import admin
from game.models import Board

class BoardAdmin(admin.ModelAdmin):
    pass

admin.site.register(Board, BoardAdmin)
