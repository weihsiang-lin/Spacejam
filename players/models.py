from django.contrib.auth.models import User
from django.db import models
from teams.models import Team, Game

class Player(models.Model):
    team = models.ForeignKey(Team)
    user = models.ForeignKey(User, null=True)
    name = models.CharField(max_length=255)
    figure = models.FileField(upload_to='players')
    number = models.PositiveSmallIntegerField()
    position = models.PositiveSmallIntegerField()
    birthday = models.DateField()
    email = models.EmailField()
    height = models.DecimalField(max_digits=4, decimal_places=1)
    weight = models.DecimalField(max_digits=4, decimal_places=1)

    def __unicode__(self):
        return self.name

class PlayerState(models.Model):
    player = models.OneToOneField(Player)
    game_played = models.PositiveIntegerField()
    game_started = models.PositiveIntegerField()
    time = models.TimeField()
    two_points_attempt = models.PositiveIntegerField()
    two_points_made = models.PositiveIntegerField()
    three_points_attempt = models.PositiveIntegerField()
    three_points_made = models.PositiveIntegerField()
    FTA = models.PositiveIntegerField()
    FTM = models.PositiveIntegerField()
    OREB = models.PositiveIntegerField()
    DREB = models.PositiveIntegerField()
    REB = models.PositiveIntegerField()
    AST = models.PositiveIntegerField()
    STL = models.PositiveIntegerField()
    BLK = models.PositiveIntegerField()
    TO = models.PositiveIntegerField()
    PF = models.PositiveIntegerField()
    PTS = models.PositiveIntegerField()

class PlayerStatePerGame(models.Model):
    player = models.ForeignKey(Player)
    game = models.ForeignKey(Game)
    game_played = models.NullBooleanField()
    game_started = models.NullBooleanField()
    time = models.TimeField()
    two_points_attempt = models.PositiveSmallIntegerField()
    two_points_made = models.PositiveSmallIntegerField()
    three_points_attempt = models.PositiveSmallIntegerField()
    three_points_made = models.PositiveSmallIntegerField()
    FTA = models.PositiveSmallIntegerField()
    FTM = models.PositiveSmallIntegerField()
    OREB = models.PositiveSmallIntegerField()
    DREB = models.PositiveSmallIntegerField()
    REB = models.PositiveSmallIntegerField()
    AST = models.PositiveSmallIntegerField()
    STL = models.PositiveSmallIntegerField()
    BLK = models.PositiveSmallIntegerField()
    TO = models.PositiveSmallIntegerField()
    PF = models.PositiveSmallIntegerField()
    PTS = models.PositiveSmallIntegerField()
