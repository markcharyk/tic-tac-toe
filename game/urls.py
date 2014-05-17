from django.conf.urls import patterns, url

urlpatterns = patterns(
    'game.views',
    url(
        r'^play/$',
        'play',
        name='play'),)