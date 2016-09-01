from django.conf.urls import url


urlpatterns = [
    url(r'^invite$', 'new_invitation', name='tictactoe_invite'),
    url(r'^invitation/(?P<pk>\d+)/$', 'accept_invitation', name='tictactoe_accept_invitation'),

    url(r'^game/(?P<pk>\d+)/$', 'game_detail', name='tictactoe_game_detail'),
]