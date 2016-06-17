from __future__ import division

import os
import time
import datetime

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone, translation
from django.utils.translation import ugettext as _
from teams.models import Team, TeamState, TeamStatePerGame, Game, Opponent, OpponentPerGame
from players.models import Player, PlayerState, PlayerStatePerGame
from spacejam import settings

def myteams(request):
    teams = Team.objects.filter(owners=request.user.id) 
    return render(request, 'teams/myteams.html', {'teams': teams})

def create_team(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        coach = request.POST.get('coach', '')
        captain = request.POST.get('captain', '')
        code = request.POST.get('code', '')

        try:
            figure = request.FILES['figure']
            team = Team(name=name, figure=figure,  coach=coach, captain=captain, code=code)
        except: # Without figure.
            team = Team(name=name, coach=coach, captain=captain, code=code)

        try:
            team.save()
        except:
            # TODO: Log system.
            # 2016.05.25 Message framework.
            messages.error(request, _('UNABLED_TO_CREATE_TEAM'))
            return HttpResponseRedirect('/teams/myteams/')

        try:
            team.owners.add(request.user)

            # 2016.04.11 Authority for edit team.
            team.administrators.add(request.user)

            # Init TeamState object.
            TeamState(team=team, game=0, two_points_attempt=0, two_points_made=0,
                      three_points_attempt=0, three_points_made=0, FTA=0, FTM=0,
                      OREB=0, DREB=0, REB=0, AST=0, STL=0, BLK=0, TO=0, PF=0,
                      PTS=0, Win=0, Lose=0).save()
        except:
            # TODO: Log system.
            # Restore Team object.
            Team.objects.get(id=team.id).delete()
            # 2016.05.25 Message framework.
            messages.error(request, _('UNABLED_TO_CREATE_TEAM'))
            return HttpResponseRedirect('/teams/myteams/')

        # 2016.05.25 Message framework.
        messages.success(request, _('TEAM_CREATED'))
        
        return HttpResponseRedirect('/teams/myteams/')
        
    return render(request, 'teams/create.html')

def edit_team(request, team_id):
    if request.method == 'POST':
        name = request.POST.get('name')
        coach = request.POST.get('coach')
        captain = request.POST.get('captain')
        code = request.POST.get('code')
        img_filepath = request.POST.get('img_filepath') # 2016.06.17 Normalize coding style.

        try:
            figure = request.FILES['figure']

            # Remove old image.
            if img_filepath != None:
                if os.path.exists(os.path.join(settings.BASE_DIR, img_filepath[1:])):
                    try:
                        os.remove(os.path.join(settings.BASE_DIR, img_filepath[1:]))
                    except:
                        # TODO: Log system.
                        # 2016.05.25 Message framework.
                        messages.error(request, _('UNABLED_TO_UPDATE_TEAM'))
                        HttpResponseRedirect('/teams/myteams/')
                
            team = Team(id=team_id, name=name, figure=figure, coach=coach, captain=captain, code=code)
        except:
            try:
                team = Team(id=team_id, name=name, figure=img_filepath, coach=coach, captain=captain, code=code)
            except:
                # TODO: Log system.
                # 2016.05.25 Message framework.
                messages.error(request, _('UNABLED_TO_UPDATE_TEAM'))
                HttpResponseRedirect('/teams/myteams/')
        try:
            team.save()
            # 2016.05.25 Message framework.
            messages.success(request, _('TEAM_UPDATED'))
        except:
            # TODO: Log system.
            # 2016.05.25 Message framework.
            messages.error(request, _('UNABLED_TO_UPDATE_TEAM'))
            return HttpResponseRedirect('/teams/myteams/')

        return HttpResponseRedirect('/teams/myteams/')
    else:
        try:
            team = Team.objects.get(id=team_id)
        except:
            # TODO: Log system.
            # 2016.05.25 Message framework.
            messages.error(request, _('UNABLED_TO_UPDATE_TEAM'))
            return HttpResponseRedirect('/teams/myteams/')

        return render(request, 'teams/edit.html', {'team': team})

def delete_team(request, team_id):
    try:
        team = Team.objects.get(id=team_id)
    except:
        # TODO: Log system.
        # 2016.05.25 Message framework.
        messages.error(request, _('UNABLED_TO_DELETE_TEAM'))
        return HttpResponseRedirect('/teams/myteams/')

    if team.figure:
        # Romove image from file system.
        filepath = os.path.join(settings.BASE_DIR, team.figure.url[1:])
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
            except:
                # TODO: Log system.
                # 2016.05.25 Message framework.
                messages.error(request, _('UNABLED_TO_DELETE_TEAM'))
                return HttpResponseRedirect('/teams/myteams/')
    try:
        # Delete team object.
        team.delete()
        # 2016.05.25 Message framework.
        messages.success(request, _('TEAM_DELETED'))
    except:
        # TODO: Log system.
        # 2016.05.25 Message framework.
        messages.error(request, _('UNABLED_TO_DELETE_TEAM'))

    return HttpResponseRedirect('/teams/myteams/')

def team_summary(request, team_id):

    past_5_games = []

    team = Team.objects.get(id=team_id)

    # Past 5 games.
    games = Game.objects.filter(team=team_id, time__lt=timezone.now()).order_by('-time')[0:5]

    # Query past 5 games' states.
    for game in games:
        past_5_game = {}
        past_5_game['game'] = game
        try:
            team_state = TeamStatePerGame.objects.get(team=team_id, game=game)
            past_5_game['team_state'] = team_state
            opponent_state = OpponentPerGame.objects.get(opponent=game.opponent.id, 
                                                         game=game)
            past_5_game['opponent_state'] = opponent_state
        except:
            # TODO: Log system.
            pass
        past_5_games.append(past_5_game)

    # Upcoming game
    upcoming_game = Game.objects.filter(team=team_id, time__gt=timezone.now()).order_by('time')

    # Roster
    players = Player.objects.filter(team=team_id).order_by('number')[0:15]

    # Team states.
    stats = TeamState.objects.get(team=team)

    # FG measurement.
    if stats.two_points_attempt or stats.three_points_attempt: # If 2PTSA and 3PTSA != 0
        FG = (stats.two_points_made + stats.three_points_made) / (stats.two_points_attempt + stats.three_points_attempt) * 100
    else:
        FG = 0.0

    if stats.game:
        # PPG measurement.
        PPG = stats.PTS / stats.game
        # APG measurement.
        AST = stats.AST / stats.game
        # RPG measurement.
        REB = stats.REB / stats.game
    else:
        PPG = AST = REB = 0.0

    return render(request, 'teams/summary.html', locals())

def mygames(request, team_id):
    team = Team.objects.get(id=team_id)

    # 2016.04.13 General team information.
    # Query team states instance.
    stats = TeamState.objects.get(team=team)

    # FG measurement.
    if stats.two_points_attempt or stats.three_points_attempt:
        FG = (stats.two_points_made + stats.three_points_made) / (stats.two_points_attempt + stats.three_points_attempt) * 100
    else:
        FG = 0.0

    if stats.game:
        # PPG measurement.
        PPG = stats.PTS / stats.game
        # AST/Game measurement.
        AST = stats.AST / stats.game
        # REB/Game measurement.
        REB = stats.REB / stats.game
    else:
        PPG = AST = REB = 0.0
    
    # 2016.04.12 Check request.user is team admin or not.
    is_admin = False
    for admin in team.administrators.all():
        if request.user == admin:
            is_admin = True
            break

    games = Game.objects.filter(team=team_id).order_by('time')
    past_games = []
    future_games = []

    for game in games:
        if game.time > timezone.now():
            future_games.append(game)
        else:
            past_game = {}
            past_game['game'] = game
            try:
                team_state = TeamStatePerGame.objects.get(team=team_id, 
                                                          game=game)
                past_game['team_state'] = team_state
                opponent_state = OpponentPerGame.objects.get(opponent=game.opponent.id, game=game)
                past_game['opponent_state'] = opponent_state
            except:
                pass
            past_games.append(past_game)

    return render(request, 'games/mygames.html', locals())

def create_game(request, team_id):

    # Query team object.
    team = Team.objects.get(id=team_id)

    if request.method == 'POST':
        opponent = request.POST.get('opponent', '')
        location = request.POST.get('location', '')
        time = request.POST.get('time')
        game_type = request.POST.get('game_type', '')
        periods = request.POST.get('periods', '')
        mins_per_period = request.POST.get('mins_per_period')
        fouls_per_player = request.POST.get('fouls_per_player')
        first_half_timeouts = request.POST.get('1st_half_timeouts')
        second_half_timeouts = request.POST.get('2nd_half_timeouts')

        # Opponent queryset
        try:
            opponent_queryset = Opponent.objects.get(team=team, name=opponent)
        except:
            opponent_queryset = Opponent(team=team, name=opponent)
            opponent_queryset.save()

        try:
            game = Game(team=team, opponent=opponent_queryset, time=time,
                        location=location, type=game_type, quarter=periods,
                        minute=mins_per_period, foul=fouls_per_player,
                        first_timeout=first_half_timeouts,
                        second_timeout=second_half_timeouts)
            game.save()
            # 2016.05.24 Message framework.
            messages.success(request, _('NEW_GAME_CREATED'))
        except:
            # TODO: Log system.
            # 2016.05.24 Message framework.
            messages.error(request, _('UNABLED_TO_CREATE_A_GAME'))
            return HttpResponseRedirect('/teams/myteams/%s/games/' % team_id)

        return HttpResponseRedirect('/teams/myteams/%s/games/' % team_id)
    else: # request.method = GET
        # 2016.04.14 General team information.
        # Query team states instance.
        stats = TeamState.objects.get(team=team)

        # FG measurement.
        if stats.two_points_attempt or stats.three_points_attempt:
            FG = (stats.two_points_made + stats.three_points_made) / (stats.two_points_attempt + stats.three_points_attempt) * 100
        else:
            FG = 0.0

        if stats.game:
            # PPG measurement.
            PPG = stats.PTS / stats.game
            # AST/Game measurement.
            AST = stats.AST / stats.game
            # REB/Game measurement.
            REB = stats.REB / stats.game
        else:
            PPG = AST = REB = 0.0

        game_time = datetime.datetime.now().isoformat()
        return render(request, 'games/create.html', locals())

def edit_game(request, team_id, game_id):

    # Query team object.
    team = Team.objects.get(id=team_id)

    if request.method == 'POST':
        opponent_id = request.POST.get('opponent_id')
        location = request.POST.get('location', '')
        time = request.POST.get('time')
        game_type = request.POST.get('game_type', '')
        periods = request.POST.get('periods', '')
        mins_per_period = request.POST.get('mins_per_period')
        fouls_per_player = request.POST.get('fouls_per_player')
        first_half_timeouts = request.POST.get('1st_half_timeouts')
        second_half_timeouts = request.POST.get('2nd_half_timeouts')

        # Query opponent object.
        opponent_instance = Opponent.objects.get(id=opponent_id)

        try:
            game = Game(id=game_id, team=team, opponent=opponent_instance, time=time, location=location, type=game_type, quarter=periods, minute=mins_per_period, foul=fouls_per_player, first_timeout=first_half_timeouts, second_timeout=second_half_timeouts)
            game.save()

            # 2016.05.24 Message framework.
            messages.success(request, _('GAME_UPDATED'))
        except:
            # TODO: Log system.
            # 2016.05.24 Message framework.
            messages.error(request, _('UNABLED_TO_UPDATE_GAME'))
            return HttpResponseRedirect('/teams/myteams/%s/games/' % team_id)

        return HttpResponseRedirect('/teams/myteams/%s/games/' % team_id)
    else: # request.method = GET
        # 2016.04.14 General team information.
        # Query team states instance.
        stats = TeamState.objects.get(team=team)

        # FG measurement.
        if stats.two_points_attempt or stats.three_points_attempt:
            FG = (stats.two_points_made + stats.three_points_made) / (stats.two_points_attempt + stats.three_points_attempt) * 100
        else:
            FG = 0.0

        if stats.game:
            # PPG measurement.
            PPG = stats.PTS / stats.game
            # AST/Game measurement.
            AST = stats.AST / stats.game
            # REB/Game measurement.
            REB = stats.REB / stats.game
        else:
            PPG = AST = REB = 0.0

        try:
            game = Game.objects.get(id=game_id)
        except:
            # TODO: Log system.
            return HttpResponseRedirect('/teams/myteams/%s/games/' % team_id)

        try:
            opponent = Opponent.objects.get(id=game.opponent_id)
        except:
            # TODO: Log system.
            return HttpResponseRedirect('/teams/myteams/%s/games/' % team_id)

        game_time_isoformat = game.time.isoformat()

        return render(request, 'games/edit.html', locals())

def edit_game_states(request, team_id, game_id):
    if request.method == "POST":
        my_q1 = request.POST.get('my_q1')
        my_q2 = request.POST.get('my_q2')
        my_q3 = request.POST.get('my_q3')
        my_q4 = request.POST.get('my_q4')
        oppo_id = request.POST.get('oppo_id')
        oppo_q1 = request.POST.get('oppo_q1')
        oppo_q2 = request.POST.get('oppo_q2')
        oppo_q3 = request.POST.get('oppo_q3')
        oppo_q4 = request.POST.get('oppo_q4')

        # 2016.05.03 Fix without overtime score issue.
        my_ot = request.POST.get('my_ot')
        oppo_ot = request.POST.get('oppo_ot')

        my_score = int(my_q1) + int(my_q2) + int(my_q3) + int(my_q4) + int(my_ot)
        oppo_score = int(oppo_q1) + int(oppo_q2) + int(oppo_q3) + int(oppo_q4) + int(oppo_ot)

        if my_score > oppo_score:
            isWin = True
        elif my_score < oppo_score:
            isWin = False
        else:
            isWin = None
    
        try:
            # Opponent object.
            opponent = Opponent.objects.get(id=oppo_id)
        except:
            # TODO: Log system.
            # 2016.05.24 Message framework.
            messages.error(request, _('UNABLED_TO_UPDATE_GAME'))
            return HttpResponseRedirect('/teams/myteams/%s/games/' % team_id)
        
        try:
            # Game object.
            game = Game.objects.get(id=game_id)
        except:
            # TODO: Log system.
            # 2016.05.24 Message framework.
            messages.error(request, _('UNABLED_TO_UPDATE_GAME'))
            return HttpResponseRedirect('/teams/myteams/%s/games/' % team_id)

        try:
            # Save opponent's stats per game.
            OpponentPerGame(opponent=opponent, game=game, score=oppo_score,
                            first_quarter_score=oppo_q1, 
                            second_quarter_score=oppo_q2,
                            third_quarter_score=oppo_q3,
                            fourth_quarter_score=oppo_q4,
                            overtime_score=oppo_ot, # 2016.05.03 Overtime issue.
                            first_quarter_foul=0, second_quarter_foul=0,
                            third_quarter_foul=0, fourth_quarter_foul=0).save()
        except:
            # TODO: Log system.
            # 2016.05.24 Message framework.
            messages.error(request, _('UNABLED_TO_UPDATE_GAME'))
            return HttpResponseRedirect('/teams/myteams/%s/games/' % team_id)
        
        # Init team states.
        team_2PTA = team_2PTM = team_3PTA = team_3PTM = team_FTA = team_FTM = 0
        team_OREB = team_DREB = team_REB = team_AST = team_STL = team_BLK = 0
        team_TO = team_PF = 0

        team_time = datetime.datetime.strptime(u'00:00', '%M:%S')

        try:
            # Query team players
            players = Player.objects.filter(team=team_id)
        except:
            # TODO: Log system.

            # 2016.05.24 Restore opponent stat per game.
            OpponentPerGame.objects.get(opponent=opponent, game=game).delete()

            # 2016.05.24 Message framework.
            messages.error(request, _('UNABLED_TO_UPDATE_GAME'))

            return HttpResponseRedirect('/teams/myteams/%s/games/' % team_id)
            
        time_default = datetime.datetime.strptime(u'00:00', '%M:%S')
        
        for p in players:
            try:
                # Player object.
                player = Player.objects.get(id=p.id)
            except:
                # TODO: Log system.
                break

            time_unicode = request.POST.get(str(p.id)+'_time')
            time = datetime.datetime.strptime(time_unicode, '%M:%S')
            if time == time_default:
                played = False
            else:
                played = True
            team_time += datetime.timedelta(minutes=time.minute,
                                            seconds=time.second)
            game_started = request.POST.get(str(p.id)+'_started')
            if game_started == "1":
                started = True
            else:
                started = False
            attempt_2pt = request.POST.get(str(p.id)+'_attempt_2pt')
            team_2PTA += int(attempt_2pt)
            made_2pt = request.POST.get(str(p.id)+'_made_2pt')
            team_2PTM += int(made_2pt)
            attempt_3pt = request.POST.get(str(p.id)+'_attempt_3pt')
            team_3PTA += int(attempt_3pt)
            made_3pt = request.POST.get(str(p.id)+'_made_3pt')
            team_3PTM += int(made_3pt)
            attempt_ft = request.POST.get(str(p.id)+'_attempt_ft')
            team_FTA += int(attempt_ft)
            made_ft = request.POST.get(str(p.id)+'_made_ft')
            team_FTM += int(made_ft)
            oreb = request.POST.get(str(p.id)+'_oreb')
            team_OREB += int(oreb)
            dreb = request.POST.get(str(p.id)+'_dreb')
            team_DREB += int(dreb)
            ast = request.POST.get(str(p.id)+'_ast')
            team_AST += int(ast)
            stl = request.POST.get(str(p.id)+'_stl')
            team_STL += int(stl)
            blk = request.POST.get(str(p.id)+'_blk')
            team_BLK += int(blk)
            to = request.POST.get(str(p.id)+'_to')
            team_TO += int(to)
            pf = request.POST.get(str(p.id)+'_pf')
            team_PF += int(pf)
            pts = int(made_2pt) * 2 + int(made_3pt) * 3 + int(made_ft) * 1

            try:
                # Save player's game states.
                PlayerStatePerGame(player=player, game=game, game_played=played,
                                   game_started=started, time=time,
                                   two_points_attempt=attempt_2pt,
                                   two_points_made=made_2pt,
                                   three_points_attempt=attempt_3pt,
                                   three_points_made=made_3pt,
                                   FTA=attempt_ft, FTM=made_ft, OREB=oreb, 
                                   DREB=dreb, REB=int(oreb)+int(dreb), 
                                   AST=ast, STL=stl,
                                   BLK=blk, TO=to, PF=pf, PTS=pts).save()
            except:
                # TODO: Log system.
                break

            # Save player's career states.
            try:
                # Query PlayerState object.
                player_state = PlayerState.objects.get(player=player)
                if played:
                    player_state.game_played += 1
                if started:
                    player_state.game_started += 1

                """
                ADD TIME
                1. Convert time object to datetime.
                2. Add datetime by timedelta function.
                """
                # Convert time object to datetime.
                datetime_obj = datetime.datetime.combine(datetime.date.today(),
                                                         player_state.time)
                # Add datetime by timedelta function.
                datetime_obj += datetime.timedelta(minutes=time.minute,
                                                   seconds=time.second)
                player_state.time = datetime_obj.time()

                player_state.two_points_attempt += int(attempt_2pt)
                player_state.two_points_made += int(made_2pt)
                player_state.three_points_attempt += int(attempt_3pt)
                player_state.three_points_made += int(made_3pt)
                player_state.FTA += int(attempt_ft)
                player_state.FTM += int(made_ft)
                player_state.OREB += int(oreb)
                player_state.DREB += int(dreb)
                player_state.REB += (int(oreb)+int(dreb))
                player_state.AST += int(ast)
                player_state.STL += int(stl)
                player_state.BLK += int(blk)
                player_state.TO += int(to)
                player_state.PF += int(pf)
                player_state.PTS += pts

                # Update player's career states.
                player_state.save()
            except:
                # TODO: Log system.

                # Restore player stats per game.
                PlayerStatePerGame.objects.get(player=player, game=game).delete() 

        try:
            # Team object.
            team = Team.objects.get(id=team_id)
        except:
            # TODO: Log system.
            team = None

        if team:
            try:
                # Save team's game states.
                TeamStatePerGame(team=team, game=game, time=team_time,
                                 two_points_attempt=team_2PTA,
                                 two_points_made=team_2PTM,
                                 three_points_attempt=team_3PTA,
                                 three_points_made=team_3PTM,
                                 FTA=team_FTA, FTM=team_FTM, OREB=team_OREB,
                                 DREB=team_DREB, 
                                 REB=int(team_OREB)+int(team_DREB),
                                 AST=team_AST, STL=team_STL, 
                                 BLK=team_BLK, TO=team_TO,
                                 first_quarter_foul=0, second_quarter_foul=0,
                                 third_quarter_foul=0, fourth_quarter_foul=0,
                                 first_quarter_score=my_q1, 
                                 second_quarter_score=my_q2,
                                 third_quarter_score=my_q3, 
                                 fourth_quarter_score=my_q4, 
                                 overtime_score=my_ot, # 2016.05.03 Overtime issue.
                                 PF=team_PF, PTS=my_score, isWin=isWin).save()
            except:
                # TODO: Log system.

                # Restore opponent stats per game.
                OpponentPerGame.objects.get(opponent=opponent, game=game).delete()

                # 2016.05.24 Message framework.
                messages.error(request, _('UNABLED_TO_UPDATE_GAME'))

                return HttpResponseRedirect('/teams/myteams/%s/games/' % team_id)

            # Save team's seasons states.
            try:
                # Query TeamState object.
                team_state = TeamState.objects.get(team=team)
                team_state.game += 1
                team_state.two_points_attempt += team_2PTA
                team_state.two_points_made += team_2PTM
                team_state.three_points_attempt += team_3PTA
                team_state.three_points_made += team_3PTM
                team_state.FTA += team_FTA
                team_state.FTM += team_FTM
                team_state.OREB += team_OREB
                team_state.DREB += team_DREB
                team_state.REB += (team_OREB + team_DREB)
                team_state.AST += team_AST
                team_state.STL += team_STL
                team_state.BLK += team_BLK
                team_state.TO += team_TO
                team_state.PF += team_PF
                team_state.PTS += my_score
                if isWin == True:
                    team_state.Win += 1
                elif isWin == False:
                    team_state.Lose += 1
                else:
                    pass

                # Update team's seasons states.
                team_state.save()
            except:
                # TODO: Log system.

                # Restore opponent stats per game.
                OpponentPerGame.objects.get(opponent=opponent, game=game).delete()

                # Restore team stats per game.
                TeamStatePerGame.objects.get(team=team, game=game).delete()

                # 2016.05.24 Message framework.
                messages.error(request, _('UNABLED_TO_UPDATE_GAME'))

                return HttpResponseRedirect('/teams/myteams/%s/games/' % team_id)

        # Update game status.
        game.isComplete = True
        game.save()

        # 2016.05.24 Message framework.
        messages.success(request, _('GAME_UPDATED'))

        return HttpResponseRedirect('/teams/myteams/%s/games/' % team_id)
    else: # request.method == GET
        try:
            game = Game.objects.get(id=game_id)
        except:
            # TODO: Log system.
            return HttpResponseRedirect('/teams/myteams/%s/games/' % team_id)
        try:
            team = Team.objects.get(id=team_id)
        except:
            # TODO: Log system.
            return HttpResponseRedirect('/teams/myteams/%s/games/' % team_id)
        try:
            players = Player.objects.filter(team=team_id).order_by('number')
        except:
            # TODO: Log system.
            return HttpResponseRedirect('/teams/myteams/%s/games/' % team_id)
        return render(request, 'games/edit_states.html', locals())

def complete_game(request, team_id, game_id):
    players_state_per_game = []
    game = Game.objects.get(id=game_id)
    team = Team.objects.get(id=team_id)

    # 2016.04.12 Check request.user is team admin or not.
    is_admin = False
    for admin in team.administrators.all():
        if request.user == admin:
            is_admin = True
            break

    try:
        team_state = TeamStatePerGame.objects.get(team=team_id, game=game)
    except:
        # TODO: Log system.
        return HttpResponseRedirect('/teams/myteams/%s/games/' % team_id)

    # 2016.05.17 Show TIME as string format.
    total_team_minutes = team_state.time.hour * 60 + team_state.time.minute
    total_team_time = str(total_team_minutes) + ":" + str(team_state.time.second)

    try:
        oppo_state = OpponentPerGame.objects.get(opponent=game.opponent.id,
                                                 game=game)
    except:
        # TODO: Log system.
        return HttpResponseRedirect('/teams/myteams/%s/games/' % team_id)

    try:
        players = Player.objects.filter(team=team_id)
    except:
        # TODO: Log system.
        return HttpResponseRedirect('/teams/myteams/%s/games/' % team_id)

    for player in players:
        try:
            player_state_per_game = PlayerStatePerGame.objects.get(player=player.id, game=game)
            # 2016.04.15 Show who's played.
            if player_state_per_game.game_played:
                players_state_per_game.append(player_state_per_game)
        except:
            # TODO: Log system.
            pass

    return render(request, 'games/complete.html', locals())

def edit_complete_game(request, team_id, game_id):
    if request.method == "POST":
        my_q1 = request.POST.get('my_q1')
        my_q2 = request.POST.get('my_q2')
        my_q3 = request.POST.get('my_q3')
        my_q4 = request.POST.get('my_q4')
        oppo_id = request.POST.get('oppo_id')
        oppo_q1 = request.POST.get('oppo_q1')
        oppo_q2 = request.POST.get('oppo_q2')
        oppo_q3 = request.POST.get('oppo_q3')
        oppo_q4 = request.POST.get('oppo_q4')

        # 2016.05.03 Fix without overtime score issue.
        my_ot = request.POST.get('my_ot')
        oppo_ot = request.POST.get('oppo_ot')

        team_state_id = request.POST.get('team_state_id')
        opponent_state_id = request.POST.get('oppo_state_id')

        my_score = int(my_q1) + int(my_q2) + int(my_q3) + int(my_q4) + int(my_ot)
        oppo_score = int(oppo_q1) + int(oppo_q2) + int(oppo_q3) + int(oppo_q4) + int(oppo_ot)

        if my_score > oppo_score:
            isWin = True
        elif my_score < oppo_score:
            isWin = False
        else:
            isWin = None # 2016.05.05 Fix if it's tied issue.

        try:
            # Opponent object.
            opponent = Opponent.objects.get(id=oppo_id)
        except:
            # TODO: Log system.
            # 2016.05.24 Message framework.
            messages.error(request, _('UNABLED_TO_UPDATE_GAME'))
            return HttpResponseRedirect('/teams/myteams/%s/games/%s/complete/' % (team_id, game_id))

        try:
            # Game object.
            game = Game.objects.get(id=game_id)
        except:
            # TODO: Log system.
            # 2016.05.24 Message framework.
            messages.error(request, _('UNABLED_TO_UPDATE_GAME'))
            return HttpResponseRedirect('/teams/myteams/%s/games/%s/complete/' % (team_id, game_id))

        try:
            # Update opponent's states per quarter.
            OpponentPerGame(id=opponent_state_id, opponent=opponent, 
                            game=game, score=oppo_score,
                            first_quarter_score=oppo_q1,
                            second_quarter_score=oppo_q2,
                            third_quarter_score=oppo_q3,
                            fourth_quarter_score=oppo_q4,
                            overtime_score=oppo_ot, # 2016.05.03 Overtime issue.
                            first_quarter_foul=0, second_quarter_foul=0,
                            third_quarter_foul=0, fourth_quarter_foul=0).save()
        except:
            # TODO: Log system.
            # 2016.05.24 Message framework.
            messages.error(request, _('UNABLED_TO_UPDATE_GAME'))
            return HttpResponseRedirect('/teams/myteams/%s/games/%s/complete/' % (team_id, game_id))

        # Init team states.
        team_2PTA = team_2PTM = team_3PTA = team_3PTM = team_FTA = team_FTM = 0
        team_OREB = team_DREB = team_REB = team_AST = team_STL = team_BLK = 0
        team_TO = team_PF = 0

        team_time = datetime.datetime.strptime(u'00:00', '%M:%S')

        # Query team players
        players = Player.objects.filter(team=team_id)

        time_default = datetime.datetime.strptime(u'00:00', '%M:%S')

        for p in players:
            try:
                # Query Player object.
                player = Player.objects.get(id=p.id)

                # Query PlayerStatePerGame object.
                old_player_state = PlayerStatePerGame.objects.get(player=p.id,
                                                                  game=game)

                time_unicode = request.POST.get(str(p.id)+'_time')
                time = datetime.datetime.strptime(time_unicode, '%M:%S')
                if time == time_default:
                    played = False
                else:
                    played = True

                team_time += datetime.timedelta(minutes=time.minute,
                                                seconds=time.second)
                game_started = request.POST.get(str(p.id)+'_started')
                if game_started == "1":
                    started = True
                else:
                    started = False
                attempt_2pt = request.POST.get(str(p.id)+'_attempt_2pt')
                team_2PTA += int(attempt_2pt)
                made_2pt = request.POST.get(str(p.id)+'_made_2pt')
                team_2PTM += int(made_2pt)
                attempt_3pt = request.POST.get(str(p.id)+'_attempt_3pt')
                team_3PTA += int(attempt_3pt)
                made_3pt = request.POST.get(str(p.id)+'_made_3pt')
                team_3PTM += int(made_3pt)
                attempt_ft = request.POST.get(str(p.id)+'_attempt_ft')
                team_FTA += int(attempt_ft)
                made_ft = request.POST.get(str(p.id)+'_made_ft')
                team_FTM += int(made_ft)
                oreb = request.POST.get(str(p.id)+'_oreb')
                team_OREB += int(oreb)
                dreb = request.POST.get(str(p.id)+'_dreb')
                team_DREB += int(dreb)
                ast = request.POST.get(str(p.id)+'_ast')
                team_AST += int(ast)
                stl = request.POST.get(str(p.id)+'_stl')
                team_STL += int(stl)
                blk = request.POST.get(str(p.id)+'_blk')
                team_BLK += int(blk)
                to = request.POST.get(str(p.id)+'_to')
                team_TO += int(to)
                pf = request.POST.get(str(p.id)+'_pf')
                team_PF += int(pf)
                pts = int(made_2pt) * 2 + int(made_3pt) * 3 + int(made_ft) * 1

                player_state_id = request.POST.get(str(p.id)+'_player_state_id')

                """ Update player's game states. """
                player_state_per_game = PlayerStatePerGame(id=player_state_id,
                                                           player=player,
                                                           game=game,
                                                           game_played=played,
                                                           game_started=started,
                                                           time=time,
                                                           two_points_attempt=attempt_2pt,
                                                           two_points_made=made_2pt,
                                                           three_points_attempt=attempt_3pt,
                                                           three_points_made=made_3pt,
                                                           FTA=attempt_ft,
                                                           FTM=made_ft,
                                                           OREB=oreb,
                                                           DREB=dreb,
                                                           REB=int(oreb)+int(dreb), 
                                                           AST=ast, STL=stl,
                                                           BLK=blk, TO=to, 
                                                           PF=pf, PTS=pts)

                """ Update player's career states. """

                # Query PlayerState object.
                player_state = PlayerState.objects.get(player=player)

                if played:
                    if not old_player_state.game_played:
                        player_state.game_played += 1
                else:
                    if old_player_state.game_played and player_state.game_played != 0:
                        player_state.game_played -=1

                if started:
                    if not old_player_state.game_started:
                        player_state.game_started += 1
                else:
                    if old_player_state.game_started and player_state.game_started != 0:
                        player_state.game_started -= 1

                """
                ADD TIME
                1. Convert time object to datetime.
                2. Add datetime by timedelta function.
                """
                # Convert time object to datetime.
                old_datetime_obj = datetime.datetime.combine(datetime.date.today(),
                                                             old_player_state.time)
                datetime_obj = datetime.datetime.combine(datetime.date.today(),
                                                         player_state.time)
                # Add datetime object by timedelta function.
                datetime_obj += datetime.timedelta(minutes=time.minute,
                                                   seconds=time.second)
                # Subtract old datetime object by timedelta function.
                datetime_obj -= datetime.timedelta(minutes=old_datetime_obj.minute,
                                                   seconds=old_datetime_obj.second)
                player_state.time = datetime_obj.time()

                player_state.two_points_attempt += (int(attempt_2pt) - old_player_state.two_points_attempt)
                player_state.two_points_made += (int(made_2pt) - old_player_state.two_points_made)
                player_state.three_points_attempt += (int(attempt_3pt) - old_player_state.three_points_attempt)
                player_state.three_points_made += (int(made_3pt) - old_player_state.three_points_made)
                player_state.FTA += (int(attempt_ft) - old_player_state.FTA)
                player_state.FTM += (int(made_ft) - old_player_state.FTM)
                player_state.OREB += (int(oreb) - old_player_state.OREB)
                player_state.DREB += (int(dreb) - old_player_state.DREB)
                player_state.REB += (int(oreb) + int(dreb) - old_player_state.REB)
                player_state.AST += (int(ast) - old_player_state.AST)
                player_state.STL += (int(stl) - old_player_state.STL)
                player_state.BLK += (int(blk) - old_player_state.BLK)
                player_state.TO += (int(to) - old_player_state.TO)
                player_state.PF += (int(pf) - old_player_state.PF)
                player_state.PTS += (pts - old_player_state.PTS)

                # Update player's game states.
                player_state_per_game.save()

                # Update player's career states.
                player_state.save()
            except:
                # TODO: Log system.
                pass
        try:    
            # Query Team object.
            team = Team.objects.get(id=team_id)
        except:
            # TODO: Log system.
            # 2016.05.24 Message framework.
            messages.error(request, _('UNABLED_TO_UPDATE_GAME'))
            return HttpResponseRedirect('/teams/myteams/%s/games/%s/complete/' % (team_id, game_id))

        try:
            # Query TeamStatePerGame object.
            old_team_state = TeamStatePerGame.objects.get(team=team, game=game)
        except:
            # TODO: Log system.
            # 2016.05.24 Message framework.
            messages.error(request, _('UNABLED_TO_UPDATE_GAME'))
            return HttpResponseRedirect('/teams/myteams/%s/games/%s/complete/' % (team_id, game_id))

        try:
            # Update team's game states.
            TeamStatePerGame(id=team_state_id, team=team, 
                             game=game, time=team_time,
                             two_points_attempt=team_2PTA,
                             two_points_made=team_2PTM,
                             three_points_attempt=team_3PTA,
                             three_points_made=team_3PTM,
                             FTA=team_FTA, FTM=team_FTM, OREB=team_OREB,
                             DREB=team_DREB, REB=int(team_OREB)+int(team_DREB),
                             AST=team_AST, STL=team_STL, BLK=team_BLK, TO=team_TO,
                             first_quarter_foul=0, second_quarter_foul=0,
                             third_quarter_foul=0, fourth_quarter_foul=0,
                             first_quarter_score=my_q1, second_quarter_score=my_q2,
                             third_quarter_score=my_q3, fourth_quarter_score=my_q4,
                             overtime_score=my_ot, # 2016.05.03 Overtime issue.
                             PF=team_PF, PTS=my_score, isWin=isWin).save()
        except:
            # TODO: Log system.
            # 2016.05.24 Message framework.
            messages.error(request, _('UNABLED_TO_UPDATE_GAME'))
            return HttpResponseRedirect('/teams/myteams/%s/games/%s/complete/' % (team_id, game_id))

        # Save team's seasons states.
        try:
            # Query TeamState object.
            team_state = TeamState.objects.get(team=team)
            if game.isComplete:
                if old_team_state.isWin != isWin:
                    if old_team_state.isWin == False and isWin == True:
                        team_state.Win += 1
                        if team_state.Lose: # If team_state.Lose > 0
                            team_state.Lose -= 1
                    elif old_team_state.isWin == None and isWin == True:
                        team_state.Win += 1
                    elif old_team_state.isWin == True and isWin == False:
                        team_state.Lose += 1
                        if team_state.Win: # If team_state.Win > 0
                            team_state.Win -= 1
                    elif old_team_state.isWin == None and isWin == False:
                        team_state.Lose += 1
                    else: # If isWin = None
                        print "isWin = None"
                        if old_team_state.isWin:
                            team_state.Win -= 1
                        elif old_team_state.isWin == False:
                            team_state.Lose -= 1
            else:
                team_state.game += 1
                if isWin == True:
                    team_state.Win += 1
                elif isWin == False:
                    team_state.Lose += 1
                else:
                    pass # 2016.05.05 Fix if it's tied issue.

            team_state.two_points_attempt += (team_2PTA - old_team_state.two_points_attempt)
            team_state.two_points_made += (team_2PTM - old_team_state.two_points_made)
            team_state.three_points_attempt += (team_3PTA - old_team_state.three_points_attempt)
            team_state.three_points_made += (team_3PTM - old_team_state.three_points_made)
            team_state.FTA += (team_FTA - old_team_state.FTA)
            team_state.FTM += (team_FTM - old_team_state.FTM)
            team_state.OREB += (team_OREB - old_team_state.OREB)
            team_state.DREB += (team_DREB - old_team_state.DREB)
            team_state.REB += (team_OREB + team_DREB - old_team_state.REB)
            team_state.AST += (team_AST - old_team_state.AST)
            team_state.STL += (team_STL - old_team_state.STL)
            team_state.BLK += (team_BLK - old_team_state.BLK)
            team_state.TO += (team_TO - old_team_state.TO)
            team_state.PF += (team_PF - old_team_state.PF)
            team_state.PTS += (my_score - old_team_state.PTS)

            # Update team's seasons states.
            team_state.save()
        except:
            # TODO: Log system.
            # 2016.05.24 Message framework.
            messages.error(request, _('UNABLED_TO_UPDATE_GAME'))
            return HttpResponseRedirect('/teams/myteams/%s/games/%s/complete/' % (team_id, game_id))

        # 2016.05.24 Message framework.
        messages.success(request, _('GAME_UPDATED'))

        return HttpResponseRedirect('/teams/myteams/%s/games/%s/complete/' % (team_id, game_id))
    else:
        players_state = []

        game = Game.objects.get(id=game_id)
        team = Team.objects.get(id=team_id)
        team_state = TeamStatePerGame.objects.get(team=team_id, game=game)
        opponent_state = OpponentPerGame.objects.get(opponent=game.opponent.id,
                                                     game=game)
        players = Player.objects.filter(team=team_id)
        
        for player in players:
            try:
                player_state  = PlayerStatePerGame.objects.get(player=player.id,
                                                               game=game)
                players_state.append(player_state)
            except:
                # TODO: Log system.
                pass
        return render(request, 'games/edit_complete.html', locals())
        

def delete_game(request, team_id, game_id): 
    try:
        # Query game object.
        game = Game.objects.get(id=game_id)
    except:
        # TODO: Log system.
        # 2016.05.24 Message framework.
        messages.error(request, _('UNABLED_TO_DELETE_GAME'))
        return HttpResponseRedirect('/teams/myteams/%s/games/' % team_id)

    if game.isComplete:
        """
        Restore player's career states and delete player's game state:
        1. Query team players.
        2. Restore each players career states.
        3. Delete each players game state.
        """
        try:
            players = Player.objects.filter(team=team_id)
        except:
            # TODO: Log system.
            # 2016.05.24 Message framework.
            messages.error(request, _('UNABLED_TO_DELETE_GAME'))
            return HttpResponseRedirect('/teams/myteams/%s/games/' % team_id)

        for player in players:
            try:
                p_state = PlayerState.objects.get(player=player)
                p_game_state = PlayerStatePerGame.objects.get(player=player.id,
                                                              game=game)
                if p_state.game_played != 0 and p_game_state.game_played:
                    p_state.game_played -= 1
                if p_state.game_started != 0 and p_game_state.game_started:
                    p_state.game_started -= 1

                # Subtract time.
                p_state_datetime = datetime.datetime.combine(datetime.datetime(1,1,1,0,0,0), p_state.time)
                p_game_state_datetime = datetime.datetime.combine(datetime.datetime(1,1,1,0,0,0), p_game_state.time)
                time_result = (p_state_datetime - p_game_state_datetime)
                p_state.time = (datetime.datetime.min + time_result).time()

                p_state.two_points_attempt -= p_game_state.two_points_attempt
                p_state.two_points_made -= p_game_state.two_points_made
                p_state.three_points_attempt -= p_game_state.three_points_attempt
                p_state.three_points_made -= p_game_state.three_points_made
                p_state.FTA -= p_game_state.FTA
                p_state.FTM -= p_game_state.FTM
                p_state.OREB -= p_game_state.OREB
                p_state.DREB -= p_game_state.DREB
                p_state.REB -= p_game_state.REB
                p_state.AST -= p_game_state.AST
                p_state.STL -= p_game_state.STL
                p_state.BLK -= p_game_state.BLK
                p_state.TO -= p_game_state.TO
                p_state.PF -= p_game_state.PF
                p_state.PTS -= p_game_state.PTS

                # Update player's career states.
                p_state.save()
                # Delete player's game state.
                p_game_state.delete()
            except:
                # TODO: Log system.
                # 2016.05.24 Message framework.
                messages.error(request, _('UNABLED_TO_DELETE_GAME'))
                return HttpResponseRedirect('/teams/myteams/%s/games/' % team_id)

        """ Restore team's season states and delete team's game state. """
        try:
            t_game_state = TeamStatePerGame.objects.get(team=team_id, game=game)
        except:
            # TODO: Log system.
            # 2016.05.24 Message framework.
            messages.error(request, _('UNABLED_TO_DELETE_GAME'))
            return HttpResponseRedirect('/teams/myteams/%s/games/' % team_id)

        if t_game_state:
            try:
                # Query Team object.
                team = Team.objects.get(id=team_id)
            except:
                # TODO: Log system.
                # 2016.05.24 Message framework.
                messages.error(request, _('UNABLED_TO_DELETE_GAME'))
                return HttpResponseRedirect('/teams/myteams/%s/games/' % team_id)

        try:
            t_state = TeamState.objects.get(team=team)
        except:
            # TODO: Log system.
            # 2016.05.24 Message framework.
            messages.error(request, _('UNABLED_TO_DELETE_GAME'))
            return HttpResponseRedirect('/teams/myteams/%s/games/' % team_id)

        if t_state:
            t_state.game -= 1
            t_state.two_points_attempt -= t_game_state.two_points_attempt
            t_state.two_points_made -= t_game_state.two_points_made
            t_state.three_points_attempt -= t_game_state.three_points_attempt
            t_state.three_points_made -= t_game_state.three_points_made
            t_state.FTA -= t_game_state.FTA
            t_state.FTM -= t_game_state.FTM
            t_state.OREB -= t_game_state.OREB
            t_state.DREB -= t_game_state.DREB
            t_state.REB -= t_game_state.REB
            t_state.AST -= t_game_state.AST
            t_state.STL -= t_game_state.STL
            t_state.BLK -= t_game_state.BLK
            t_state.TO -= t_game_state.TO
            t_state.PF -= t_game_state.PF
            t_state.PTS -= t_game_state.PTS

            if t_game_state.isWin:
                t_state.Win -= 1
            elif t_game_state.isWin == False:
                t_state.Lose -= 1
            else:
                pass # 2016.05.05 Fix if it's tied issue.

            try:
                # Update team's season states.
                t_state.save()
            except:
                # TODO: Log system.
                # 2016.05.24 Message framework.
                messages.error(request, _('UNABLED_TO_DELETE_GAME'))
                return HttpResponseRedirect('/teams/myteams/%s/games/' % team_id)

            try:
                # Delete team's game state.
                t_game_state.delete()
            except:
                # TODO: Log system.
                # 2016.05.24 Message framework.
                messages.error(request, _('UNABLED_TO_DELETE_GAME'))
                return HttpResponseRedirect('/teams/myteams/%s/games/' % team_id)

    try:
        # Finally, delete game object.
        game.delete()
        # 2016.05.24 Message framework.
        messages.success(request, _('GAME_DELETED'))
    except:
        # TODO: Log system.
        # 2016.05.24 Message framework.
        messages.error(request, _('UNABLED_TO_DELETE_GAME'))
        return HttpResponseRedirect('/teams/myteams/%s/games/' % team_id)

    return HttpResponseRedirect('/teams/myteams/%s/games/' % team_id)

def stats(request, team_id):
    team = Team.objects.get(id=team_id)
    stats = TeamState.objects.get(team=team)
    if stats.two_points_attempt or stats.three_points_attempt:
        # 2016.04.13 Normalize variable.
        FG = (stats.two_points_made + stats.three_points_made) / (stats.two_points_attempt + stats.three_points_attempt) * 100
    else:
        FG = 0.0
    if stats.three_points_attempt:
        three_points_percentage =  stats.three_points_made / stats.three_points_attempt * 100
    else:
        three_points_percentage = 0.0
    if stats.FTA:
        free_throw_percentage = stats.FTM / stats.FTA * 100
    else:
        free_throw_percentage = 0.0
    if stats.game:
        oreb_avg = stats.OREB / stats.game
        dreb_avg = stats.DREB / stats.game
        REB = (stats.OREB + stats.DREB) / stats.game # 2016.04.13 Normalize variable.
        AST = stats.AST / stats.game # 2016.04.13 Normalize variable.
        stl_avg = stats.STL / stats.game
        blk_avg = stats.BLK / stats.game
        to_avg = stats.TO / stats.game
        pf_avg = stats.PF / stats.game
        PPG = stats.PTS / stats.game # 2016.04.13 Normalize variable.

        # 2016.05.05 FGA, 3PTSA, FTA average measurements.
        FGA_avg = (stats.two_points_attempt + stats.three_points_attempt) / stats.game
        threePTSA_avg = stats.three_points_attempt / stats.game
        FTA_avg = stats.FTA / stats.game
    else:
        oreb_avg = dreb_avg = REB = AST = stl_avg = 0.0
        blk_avg = to_avg = pf_avg = PPG = 0.0
        # 2016.05.05 FGA, 3PTSA, FTA average measurements.
        FGA_avg = threePTSA_avg = FTA_avg = 0.0
    return render(request, 'teams/stats.html', locals())
