# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('figure', models.FileField(upload_to=b'players')),
                ('number', models.PositiveSmallIntegerField()),
                ('position', models.PositiveSmallIntegerField()),
                ('birthday', models.DateField()),
                ('email', models.EmailField(max_length=254)),
                ('height', models.DecimalField(max_digits=4, decimal_places=1)),
                ('weight', models.DecimalField(max_digits=4, decimal_places=1)),
                ('team', models.ForeignKey(to='teams.Team')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PlayerState',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('game_played', models.PositiveIntegerField()),
                ('game_started', models.PositiveIntegerField()),
                ('time', models.TimeField()),
                ('two_points_attempt', models.PositiveIntegerField()),
                ('two_points_made', models.PositiveIntegerField()),
                ('three_points_attempt', models.PositiveIntegerField()),
                ('three_points_made', models.PositiveIntegerField()),
                ('FTA', models.PositiveIntegerField()),
                ('FTM', models.PositiveIntegerField()),
                ('OREB', models.PositiveIntegerField()),
                ('DREB', models.PositiveIntegerField()),
                ('REB', models.PositiveIntegerField()),
                ('AST', models.PositiveIntegerField()),
                ('STL', models.PositiveIntegerField()),
                ('BLK', models.PositiveIntegerField()),
                ('TO', models.PositiveIntegerField()),
                ('PF', models.PositiveIntegerField()),
                ('PTS', models.PositiveIntegerField()),
                ('player', models.OneToOneField(to='players.Player')),
            ],
        ),
        migrations.CreateModel(
            name='PlayerStatePerGame',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('game_played', models.NullBooleanField()),
                ('game_started', models.NullBooleanField()),
                ('time', models.TimeField()),
                ('two_points_attempt', models.PositiveSmallIntegerField()),
                ('two_points_made', models.PositiveSmallIntegerField()),
                ('three_points_attempt', models.PositiveSmallIntegerField()),
                ('three_points_made', models.PositiveSmallIntegerField()),
                ('FTA', models.PositiveSmallIntegerField()),
                ('FTM', models.PositiveSmallIntegerField()),
                ('OREB', models.PositiveSmallIntegerField()),
                ('DREB', models.PositiveSmallIntegerField()),
                ('REB', models.PositiveSmallIntegerField()),
                ('AST', models.PositiveSmallIntegerField()),
                ('STL', models.PositiveSmallIntegerField()),
                ('BLK', models.PositiveSmallIntegerField()),
                ('TO', models.PositiveSmallIntegerField()),
                ('PF', models.PositiveSmallIntegerField()),
                ('PTS', models.PositiveSmallIntegerField()),
                ('game', models.ForeignKey(to='teams.Game')),
                ('player', models.ForeignKey(to='players.Player')),
            ],
        ),
    ]
