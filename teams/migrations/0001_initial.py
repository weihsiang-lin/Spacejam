# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.DateTimeField()),
                ('location', models.CharField(max_length=255)),
                ('type', models.PositiveSmallIntegerField()),
                ('quarter', models.PositiveSmallIntegerField()),
                ('minute', models.PositiveSmallIntegerField()),
                ('foul', models.PositiveSmallIntegerField()),
                ('first_timeout', models.PositiveSmallIntegerField()),
                ('second_timeout', models.PositiveSmallIntegerField()),
                ('isComplete', models.NullBooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Opponent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('figure', models.FileField(upload_to=b'opponents')),
            ],
        ),
        migrations.CreateModel(
            name='OpponentPerGame',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.PositiveSmallIntegerField()),
                ('first_quarter_score', models.PositiveSmallIntegerField()),
                ('second_quarter_score', models.PositiveSmallIntegerField()),
                ('third_quarter_score', models.PositiveSmallIntegerField()),
                ('fourth_quarter_score', models.PositiveSmallIntegerField()),
                ('overtime_score', models.PositiveSmallIntegerField()),
                ('first_quarter_foul', models.PositiveSmallIntegerField()),
                ('second_quarter_foul', models.PositiveSmallIntegerField()),
                ('third_quarter_foul', models.PositiveSmallIntegerField()),
                ('fourth_quarter_foul', models.PositiveSmallIntegerField()),
                ('game', models.OneToOneField(to='teams.Game')),
                ('opponent', models.ForeignKey(to='teams.Opponent')),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('figure', models.FileField(upload_to=b'teams')),
                ('coach', models.CharField(max_length=70)),
                ('captain', models.CharField(max_length=70)),
                ('code', models.CharField(max_length=5)),
                ('administrators', models.ManyToManyField(related_name='administrates', to=settings.AUTH_USER_MODEL)),
                ('owners', models.ManyToManyField(related_name='owns', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TeamState',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('game', models.PositiveIntegerField()),
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
                ('Win', models.PositiveIntegerField()),
                ('Lose', models.PositiveIntegerField()),
                ('team', models.OneToOneField(to='teams.Team')),
            ],
        ),
        migrations.CreateModel(
            name='TeamStatePerGame',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
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
                ('first_quarter_foul', models.PositiveSmallIntegerField()),
                ('second_quarter_foul', models.PositiveSmallIntegerField()),
                ('third_quarter_foul', models.PositiveSmallIntegerField()),
                ('fourth_quarter_foul', models.PositiveSmallIntegerField()),
                ('PF', models.PositiveSmallIntegerField()),
                ('first_quarter_score', models.PositiveSmallIntegerField()),
                ('second_quarter_score', models.PositiveSmallIntegerField()),
                ('third_quarter_score', models.PositiveSmallIntegerField()),
                ('fourth_quarter_score', models.PositiveSmallIntegerField()),
                ('overtime_score', models.PositiveSmallIntegerField()),
                ('PTS', models.PositiveSmallIntegerField()),
                ('isWin', models.NullBooleanField()),
                ('game', models.OneToOneField(to='teams.Game')),
                ('team', models.ForeignKey(to='teams.Team')),
            ],
        ),
        migrations.AddField(
            model_name='opponent',
            name='team',
            field=models.ForeignKey(to='teams.Team'),
        ),
        migrations.AddField(
            model_name='game',
            name='opponent',
            field=models.ForeignKey(to='teams.Opponent'),
        ),
        migrations.AddField(
            model_name='game',
            name='team',
            field=models.ForeignKey(to='teams.Team'),
        ),
    ]
