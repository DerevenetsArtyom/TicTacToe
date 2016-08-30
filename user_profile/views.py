from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from tictactoe.models import Game


@login_required
def home(request):
    my_games = Game.objects.games_for_user(request.user)  # Games for current user

    active_games = my_games.filter(status="A")  # Filter by active status
    finished_games = my_games.exclude(status="A")  # Excluding active games

    waiting_games = active_games.filter(next_to_move=request.user)  # My turn
    other_games = active_games.exclude(next_to_move=request.user)  # Isn't my turn
    context = {'other_games': other_games,
                'waiting_games': waiting_games,
                'finished_games': finished_games}
    return render(request, "user_profile/home.html", context)