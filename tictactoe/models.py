from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.urlresolvers import reverse

# Choices for status
GAME_STATUS_CHOICES = (
    ('A', 'Active'),
    ('F', 'First Player Wins'),
    ('S', 'Second Player Wins'),
    ('D', 'Draw')
)

FIRST_PLAYER_MOVE = 'X'
SECOND_PLAYER_MOVE = 'O'
BOARD_SIZE = 3


class GamesManager(models.Manager):
    def games_for_user(self, user):
        """Return a queryset of games that this user participates in"""
        return super(GamesManager, self).get_queryset().filter(
            Q(first_player_id=user.id) | Q(second_player_id=user.id))

    # Create a new game for two players
    def new_game(self, invitation):
        game = Game(first_player=invitation.to_user,
                    second_player=invitation.from_user,
                    next_to_move=invitation.to_user)
        return game


class Game(models.Model):
    first_player = models.ForeignKey(User, related_name="games_first_player")
    second_player = models.ForeignKey(User, related_name="games_second_player")
    next_to_move = models.ForeignKey(User, related_name="games_to_move")
    start_time = models.DateTimeField(auto_now_add=True)
    last_active = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=1, default='A',
                              choices=GAME_STATUS_CHOICES)
    objects = GamesManager()

    def __str__(self):
        return "{0} vs {1}".format(self.first_player, self.second_player)

    def as_board(self):
            """Return a representation of the game board as a two-dimensional list,
            so you can ask for the state of a square at position [y][x].

            It will contain a list of lines, where every line is a list of
            'X', 'O', or ''. For example, a 3x3 board position:

            [['', 'X', ''],
             ['O', '', ''],
             ['X', '', '']]"""
            board = [['' for x in range(BOARD_SIZE)] for y in range(BOARD_SIZE)]
            for move in self.move_set.all():
                board[move.y][move.x] = FIRST_PLAYER_MOVE if move.by_first_player else SECOND_PLAYER_MOVE
            return board

    # Return the last move of the game using 'latest'
    def last_move(self):
        # 'latest' use 'get_latest_by' field of model
        return self.move_set.latest()

    def get_absolute_url(self):
        return reverse('tictactoe_game_detail', args=[self.id])


class Move(models.Model):
    x = models.IntegerField()
    y = models.IntegerField()
    comment = models.CharField(max_length=300)
    by_first_player = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True)
    game = models.ForeignKey(Game)

    class Meta:
        # used for 'latest' method to determine the latest move
        get_latest_by = 'timestamp'

    # Whose turn is
    def player(self):
        return self.game.first_player if self.by_first_player else self.game.second_player


class Invitation(models.Model):
    from_user = models.ForeignKey(User, related_name="invitations_sent")
    to_user = models.ForeignKey(User, related_name="invitations_received",
                                verbose_name="User to invite",
                                help_text="Please select the user you want to play a game with")
    message = models.CharField("Optional Message", max_length=300, blank=True,
                               help_text="Adding a friendly message is never a bad idea!")
    timestamp = models.DateTimeField(auto_now_add=True)
