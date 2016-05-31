from django.db import models
from django.contrib.auth.models import User

class Team(models.Model):
    name = models.CharField(max_length=255)
    figure = models.FileField(upload_to='teams')
    coach = models.CharField(max_length=70)
    captain = models.CharField(max_length=70)
    code = models.CharField(max_length=5)
    owners = models.ManyToManyField(User, related_name='owns')
    administrators = models.ManyToManyField(User, related_name='administrates')
    
    def __unicode__(self):
        return self.name

class TeamState(models.Model):
    team = models.OneToOneField(Team)
    game = models.PositiveIntegerField()
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
    Win = models.PositiveIntegerField()
    Lose = models.PositiveIntegerField()

class Opponent(models.Model):
    team = models.ForeignKey(Team)
    name = models.CharField(max_length=255)
    figure = models.FileField(upload_to='opponents')

    def __unicode__(self):
        return self.name

class Game(models.Model):
    team = models.ForeignKey(Team)
    opponent = models.ForeignKey(Opponent)
    time = models.DateTimeField()
    location = models.CharField(max_length=255)
    type = models.PositiveSmallIntegerField()
    quarter = models.PositiveSmallIntegerField()
    minute = models.PositiveSmallIntegerField()
    foul = models.PositiveSmallIntegerField()
    first_timeout = models.PositiveSmallIntegerField()
    second_timeout = models.PositiveSmallIntegerField()
    isComplete = models.NullBooleanField()

class TeamStatePerGame(models.Model):
    team = models.ForeignKey(Team)
    game = models.OneToOneField(Game)
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
    first_quarter_foul = models.PositiveSmallIntegerField()
    second_quarter_foul = models.PositiveSmallIntegerField()
    third_quarter_foul = models.PositiveSmallIntegerField()
    fourth_quarter_foul = models.PositiveSmallIntegerField()
    PF = models.PositiveSmallIntegerField()
    first_quarter_score = models.PositiveSmallIntegerField()
    second_quarter_score = models.PositiveSmallIntegerField()
    third_quarter_score = models.PositiveSmallIntegerField()
    fourth_quarter_score = models.PositiveSmallIntegerField()
    overtime_score = models.PositiveSmallIntegerField()
    PTS = models.PositiveSmallIntegerField()
    isWin = models.NullBooleanField()

class OpponentPerGame(models.Model):
    opponent = models.ForeignKey(Opponent)
    game = models.OneToOneField(Game)
    score = models.PositiveSmallIntegerField()
    first_quarter_score = models.PositiveSmallIntegerField()
    second_quarter_score = models.PositiveSmallIntegerField()
    third_quarter_score = models.PositiveSmallIntegerField()
    fourth_quarter_score = models.PositiveSmallIntegerField()
    overtime_score = models.PositiveSmallIntegerField()
    first_quarter_foul = models.PositiveSmallIntegerField()
    second_quarter_foul = models.PositiveSmallIntegerField()
    third_quarter_foul = models.PositiveSmallIntegerField()
    fourth_quarter_foul = models.PositiveSmallIntegerField()
