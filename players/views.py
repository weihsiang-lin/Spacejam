from __future__ import division, unicode_literals

import os
import datetime

from django.contrib import messages
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils.encoding import smart_unicode # 2016.05.31 Fix send Chinese email issue.
from django.utils.translation import ugettext as _
from teams.models import Team, TeamState, Game, Opponent
from players.models import Player, PlayerState, PlayerStatePerGame
from spacejam import settings

# Team roster.
def index(request, team_id):
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
        # APG measurement.
        AST = stats.AST / stats.game
        # RPG measurement.
        REB = stats.REB / stats.game
    else:
        PPG = AST = REB = 0.0

    # 2016.04.12 Check request.user is team admin or not.
    is_admin = False
    for admin in team.administrators.all():
        if request.user == admin:
            is_admin = True
            break

    # Players queryset.
    players = Player.objects.filter(team=team_id).order_by('number')

    return render(request, 'teams/roster.html', locals())

def create(request, team_id):
    if request.method == "POST":
        name = request.POST.get('name')
        number = request.POST.get('number')
        position = request.POST.get('position')
        height = request.POST.get('height', '')
        weight = request.POST.get('weight', '')
        birthday = request.POST.get('birthday', '')
        email = request.POST.get('email', '')
        #isAdmin = request.POST.get('isAdmin')

        # Team instance
        try:
            team = Team.objects.get(id=team_id)
        except:
            team = None

        if team:
            try:
                image = request.FILES['image']
                player = Player(team=team, name=name, number=number, 
                                figure=image, position=position, birthday=birthday,
                                email=email, height=height, weight=weight)
            except: # Without image.
                player = Player(team=team, name=name, number=number, 
                                position=position, birthday=birthday, email=email, 
                                height=height, weight=weight)

        #if isAdmin == "true":
        #    player.isAdmin = True
        #else:
        #    player.isAdmin = False

            try:
                player.save()
            except:
                # TODO: Log system.
                # 2016.05.24 Message framework.
                messages.error(request, _('UNABLED_TO_CREATE_PLAYER'))
                return redirect('player_index', team_id=team_id)
 
        #player.team.add(team)

        # Init time.
        time = datetime.datetime.strptime(u'00:00', '%M:%S')

        try:
            # Init PlayerState object.
            PlayerState(player=player, game_played=0, game_started=0, time=time,
                        two_points_attempt=0, two_points_made=0,
                        three_points_attempt=0, three_points_made=0,
                        FTA=0, FTM=0, OREB=0, DREB=0, REB=0, AST=0, STL=0, BLK=0,
                        TO=0, PF=0, PTS=0).save()
        except:
            # TODO: Log system.

            # Restore player.
            Player.objects.get(team=team, name=name).delete()

            # 2016.05.24 Message framework.
            messages.error(request, _('UNABLED_TO_CREATE_PLAYER'))
            return redirect('player_index', team_id=team_id)

        # Send invitation mail.
        if email:
            try:
                # 2016.05.17 Version 1 email.
                subject = "Welcome to the DataHoops - Sign Up and Join the Team"
                from_email = settings.DEFAULT_FROM_EMAIL
                to = email
                html_content = "<h2>Welcome to the DataHoops!</h2><p>Hi "+smart_unicode(name)+",</p><p>You can use DataHoops to track your stats and improve your game!</p><p>To get started, <a href='http://www.datahoops.com/teams/myteams/"+str(team_id)+"/players/"+str(player.id)+"/invitation/'>click to log in/register</a> now.</p>"
                msg = EmailMessage(subject, html_content, from_email, [to])
                msg.content_subtype = "html"
                msg.send()
            except:
                # TODO: Log system.
                pass

        # 2016.05.24 Message framework.
        messages.success(request, _('PLAYER_CREATED'))

        return HttpResponseRedirect('/teams/myteams/%s/players/' % team_id)
    else:
        # 2016.04.14 General team information.
        # Query team instance.
        team = Team.objects.get(id=team_id)

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

        return render(request, 'players/create.html', locals())

def edit(request, team_id, player_id):
    if request.method == "POST":
        name = request.POST.get('name')
        number = request.POST.get('number')
        position = request.POST.get('position')
        height = request.POST.get('height')
        weight = request.POST.get('weight')
        birthday = request.POST.get('birthday')
        email = request.POST.get('email')

        #isAdmin = request.POST.get('isAdmin')

        # Filepath of image if it's existed.
        filepath = request.POST.get('filepath')

        # Query Player instance.
        try:
            player = Player.objects.get(id=player_id)
        except:
            player = None

            # TODO: Log system.

            # 2016.05.25 Message framework.
            messages.error(request, _('UNABLED_TO_UPDATE_PLAYER'))

        if player:
            player.name = name
            player.number = number
            player.position = position
            player.birthday = birthday
            player.email = email
            player.height = height
            player.weight = weight

            try:
                image = request.FILES['image']
            
                # Remove old image.
                if filepath != '':
                    abs_filepath = os.path.join(settings.BASE_DIR, filepath)[1:]
                    if os.path.exists(abs_filepath):
                        os.remove(abs_filepath)

                player.figure = image

            #player = Player(id=player_id, team=team_id, name=name, figure=image,
            #                number=number, position=position, birthday=birthday,
            #                email=email, height=height, weight=weight)

            except: # Without image.
                player.figure = filepath

            #player = Player(id=player_id, team=team_id, name=name, 
            #                figure=filepath, number=number, position=position, 
            #                birthday=birthday, email=email, height=height, 
            #                weight=weight)

            try:
                player.save()
            except:
                # Failed to edit user.
                # TODO: Log system.
                # 2016.05.25 Message framework.
                messages.error(request, _('UNABLED_TO_UPDATE_PLAYER'))
                return HttpResponseRedirect('/teams/myteams/%s/players/' % team_id)

            """
            If player is connected to an user then player can be selected as
            an administrators or not.
            """
            if player.user:
                try:
                    team = Team.objects.get(id=team_id)
                except:
                    team = null
                    # 2016.05.25 Message framework.
                    messages.error(request, _('UNABLED_TO_UPDATE_PLAYER'))

                if team:
                    isAdmin = request.POST.get("isAdmin")
                    if isAdmin == "true":
                        team.administrators.add(player.user)
                #player.isAdmin = True
                #else:
                    #player.isAdmin = False
            else:
                # Send invitation email if player.user is None. 
                if email:
                    try:
                        # 2016.05.17 Version 1 email.
                        subject = "Welcome to the DataHoops - Sign Up and Join the Team"
                        from_email = settings.DEFAULT_FROM_EMAIL
                        to = email
                        html_content = "<h2>Welcome to the DataHoops!</h2><p>Hi "+smart_unicode(name)+",</p><p>You can use DataHoops to track your stats and improve your game!</p><p>To get started, <a href='http://www.datahoops.com/teams/myteams/"+str(team_id)+"/players/"+str(player.id)+"/invitation/'>click to log in/register</a> now.</p>"
                        msg = EmailMessage(subject, html_content, from_email, [to])
                        msg.content_subtype = "html"
                        msg.send()
                    except:
                        # TODO: Log system.
                        pass

        #player.team.add(team)

        # 2016.05.25 Message framework.
        messages.success(request, _('PLAYER_UPDATED'))

        return HttpResponseRedirect('/teams/myteams/%s/players/' % team_id)
    else: # request method = GET
        # Init. default variable.
        is_admin = False

        try:
            team = Team.objects.get(id=team_id)
        except:
            # TODO: Log system.
            team = None

        if team:
            for administrator in team.administrators.all():
                if administrator == request.user:
                    is_admin = True
                    break

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
                # APG measurement.
                AST = stats.AST / stats.game
                # RPG measurement.
                REB = stats.REB / stats.game
            else:
                PPG = AST = REB = 0.0

        try:
            player = Player.objects.get(id=player_id)
        except:
            # TODO: Log system.
            player = None

        if player:
            birthday = player.birthday.isoformat()

        return render(request, 'players/edit.html', locals())

def delete(request, team_id, player_id):
    try:
        player = Player.objects.get(id=player_id)
    except:
        # TODO: Log system.
        # 2016.05.25 Message framework.
        messages.error(request, _('UNABLED_TO_DELETE_PLAYER'))
        return HttpResponseRedirect('/teams/myteams/%s/players/' % team_id)

    if player.figure:
        # Remove image from file system.
        filepath = os.path.join(settings.BASE_DIR, player.figure.url[1:])
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
            except:
                # TODO: Log system.
                # 2016.05.25 Message framework.
                messages.error(request, _('UNABLED_TO_DELETE_PLAYER'))
                return HttpResponseRedirect('/teams/myteams/%s/players/' % team_id)
                
    try:
        # Delete player object.
        player.delete()
    except:
        # TODO: Log system.
        # 2016.05.25 Message framework.
        messages.error(request, _('UNABLED_TO_DELETE_PLAYER'))
        return HttpResponseRedirect('/teams/myteams/%s/players/' % team_id)

    # 2016.05.25 Message framework.
    messages.success(request, _('PLAYER_DELETED'))

    return HttpResponseRedirect('/teams/myteams/%s/players/' % team_id)

def summary(request, team_id, player_id):
    team = Team.objects.get(id=team_id)

    player = Player.objects.get(id=player_id, team=team)

    try:
        # Player's career stats.
        stats = PlayerState.objects.get(player=player)
    except:
        # TODO: Log system.
        stats = None

    # 2016.05.17 Show TIME as string format
    if stats:
        total_stats_minutes = stats.time.hour * 60 + stats.time.minute
        total_stats_time = str(total_stats_minutes) + ":" + str(stats.time.second)
    else:
        total_stats_time = "00:00"

    # Player's career avg. stats measurement.
    if stats.two_points_attempt or stats.three_points_attempt:
        career_FG_avg = (stats.two_points_made + stats.three_points_made) / (stats.two_points_attempt + stats.three_points_attempt) * 100
    else:
        career_FG_avg = 0.0
    if stats.three_points_attempt:
        career_3PT_avg = stats.three_points_made / stats.three_points_attempt * 100
    else:
        career_3PT_avg = 0.0
    if stats.FTA:
        career_FT_avg = stats.FTM / stats.FTA * 100
    else:
        career_FT_avg = 0.0

    if stats.game_played:
        # Time measurement
        career_total_seconds = stats.time.hour * 3600 + stats.time.minute * 60 + stats.time.second
        career_avg_seconds = career_total_seconds / stats.game_played
        career_minutes, career_seconds = divmod(int(career_avg_seconds), 60)
        career_time_avg = datetime.time(0, career_minutes, career_seconds)

        career_OREB_avg = stats.OREB / stats.game_played
        career_DREB_avg = stats.DREB / stats.game_played
        career_REB_avg = stats.REB / stats.game_played
        career_AST_avg = stats.AST / stats.game_played
        career_STL_avg = stats.STL / stats.game_played
        career_BLK_avg = stats.BLK / stats.game_played
        career_TO_avg = stats.TO / stats.game_played
        career_PF_avg = stats.PF / stats.game_played
        career_PTS_avg = stats.PTS / stats.game_played
    else:
        career_OREB_avg = career_DREB_avg = career_REB_avg = 0.0
        career_AST_avg = career_STL_avg = career_BLK_avg = 0.0
        career_TO_avg = career_PF_avg = career_PTS_avg = 0.0
        career_time_avg = datetime.time(0, 0, 0)

    # Player's stats of past 5 games.
    past_five_games = PlayerStatePerGame.objects.filter(player=player_id).order_by('-game_id__time').exclude(time=datetime.time(0, 0, 0))[0:5]

    past_five_games_avg = {} # Dictionary of average stats.
    past_five_games_total = {} # Dictionary of total stats.

    past_five_games_list = [] # List of past five games' data.

    # Init. stats.
    FGM = FGA = M_3PT = A_3PT = FTM = FTA = 0
    OREB = DREB = REB = AST = STL = BLK = TO = PF = PTS = 0
    
    five_games_seconds = 0

    for past_five_game in past_five_games:
        game_data = {} # Dictionary of game data.

        # Total stats measurement.
        FGM += (past_five_game.two_points_made + past_five_game.three_points_made)
        FGA += (past_five_game.two_points_attempt + past_five_game.three_points_attempt)
        M_3PT += past_five_game.three_points_made
        A_3PT += past_five_game.three_points_attempt
        FTM += past_five_game.FTM
        FTA += past_five_game.FTA
        OREB += past_five_game.OREB
        DREB += past_five_game.DREB
        REB += (past_five_game.OREB + past_five_game.DREB)
        AST += past_five_game.AST
        STL += past_five_game.STL
        BLK += past_five_game.BLK
        TO += past_five_game.TO
        PF += past_five_game.PF
        PTS += past_five_game.PTS
        five_games_seconds += (past_five_game.time.minute * 60 + past_five_game.time.second)

        # Save each game's data
        game_data['obj'] = past_five_game
        if past_five_game.two_points_attempt or past_five_game.three_points_attempt:
            game_data['FG_Percent'] = (past_five_game.two_points_made + past_five_game.three_points_made) / (past_five_game.two_points_attempt + past_five_game.three_points_attempt) * 100
        else:
            game_data['FG_Percent'] = 0.0
        if past_five_game.three_points_attempt:
            game_data['3PT_Percent'] = past_five_game.three_points_made / past_five_game.three_points_attempt * 100
        else:
            game_data['3PT_Percent'] = 0.0
        if past_five_game.FTA:
            game_data['FT_Percent'] = past_five_game.FTM / past_five_game.FTA * 100
        else:
            game_data['FT_Percent'] = 0.0

        past_five_games_list.append(game_data)

    # Save total stats.
    past_five_games_total['FGM'] = FGM
    past_five_games_total['FGA'] = FGA
    past_five_games_total['M_3PT'] = M_3PT
    past_five_games_total['A_3PT'] = A_3PT
    past_five_games_total['FTM'] = FTM
    past_five_games_total['FTA'] = FTA
    past_five_games_total['OREB'] = OREB
    past_five_games_total['DREB'] = DREB
    past_five_games_total['REB'] = REB
    past_five_games_total['AST'] = AST
    past_five_games_total['STL'] = STL
    past_five_games_total['BLK'] = BLK
    past_five_games_total['TO'] = TO
    past_five_games_total['PF'] = PF
    past_five_games_total['PTS'] = PTS
    
    total_minutes, total_seconds = divmod(int(five_games_seconds), 60)
    past_five_games_total['time'] = str(total_minutes) + ":" + str(total_seconds) # 2016.05.17 Show total TIME as string format.

    # Save avg. stats.
    if len(past_five_games):
        past_five_games_avg['FGM'] = FGM / len(past_five_games)
        past_five_games_avg['FGA'] = FGA / len(past_five_games)
        if FGA:
            past_five_games_avg['FG_Percent'] = FGM / FGA * 100
        else:
            past_five_games_avg['FG_Percent'] = 0.0
        past_five_games_avg['M_3PT'] = M_3PT / len(past_five_games)
        past_five_games_avg['A_3PT'] = A_3PT / len(past_five_games)
        if A_3PT:
            past_five_games_avg['3PT_Percent'] = M_3PT / A_3PT * 100
        else:
            past_five_games_avg['3PT_Percent'] = 0.0
        past_five_games_avg['FTM'] = FTM / len(past_five_games)
        past_five_games_avg['FTA'] = FTA / len(past_five_games)
        if FTA:
            past_five_games_avg['FT_Percent'] = FTM / FTA * 100
        else:
            past_five_games_avg['FT_Percent'] = 0.0
        past_five_games_avg['OREB'] = OREB / len(past_five_games)
        past_five_games_avg['DREB'] = DREB / len(past_five_games)
        past_five_games_avg['REB'] = REB / len(past_five_games)
        past_five_games_avg['AST'] = AST / len(past_five_games)
        past_five_games_avg['STL'] = STL / len(past_five_games)
        past_five_games_avg['BLK'] = BLK / len(past_five_games)
        past_five_games_avg['TO'] = TO / len(past_five_games)
        past_five_games_avg['PF'] = PF / len(past_five_games)
        past_five_games_avg['PTS'] = PTS / len(past_five_games)

        avg_five_games_seconds = five_games_seconds / len(past_five_games)
        avg_minutes, avg_seconds = divmod(int(avg_five_games_seconds), 60)
        past_five_games_avg['time'] = datetime.time(0, avg_minutes, avg_seconds)

    # 2016.05.05 Performance measurement with teammates.
    team_stats = TeamState.objects.get(team=team)

    if team_stats.game:
        # Team PPG measurement.
        team_PPG = team_stats.PTS / team_stats.game
        # Team AST/Game measurement.
        team_AST = team_stats.AST / team_stats.game
        # Team REB/Game measurement.
        team_REB = team_stats.REB / team_stats.game
    else:
        team_PPG = team_AST = team_REB = 0.0
    
    PER_PPG = team_PPG - career_PTS_avg
    PER_AST = team_AST - career_AST_avg
    PER_REB = team_REB - career_REB_avg

    return render(request, 'players/summary.html', locals())

def invitation(request, team_id, player_id):
    return HttpResponseRedirect('/accounts/login/?Invitation=True&Team='+team_id+'&Player='+player_id)

def invite_registration(request, team_id, player_id):
    if request.method == "POST":
        """ Let request.user join team. """
        try:
            team = Team.objects.get(id=team_id)
        except:
            team = None
        if team:
            team_code = request.POST.get('team_code')
            if team.code == team_code:
                team.owners.add(request.user)
        """ Connect player to request.user """
        p_id = request.POST.get('player_id')
        try:
            player = Player.objects.get(id=int(p_id))
        except:
            player = None
        if player:
            player.user = request.user
            player.save()
        return redirect('team_summary', team_id=team_id)
    else:
        team = Team.objects.get(id=team_id)
        player = Player.objects.get(id=player_id)
        return render(request, 'teams/registration.html', locals())
