from django.conf.urls import patterns, url

urlpatterns = patterns(
    'game.views',
    url(
        r'^play/$',
        'play',
        name='play'),
    url(
        r'^play/move/$',
        'move',
        name='move'),)