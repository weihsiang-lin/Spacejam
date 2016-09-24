from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response, redirect
from django.utils.translation import ugettext as _

from teams.models import Team

def index(request):
    return render(request, 'index.html')

# 2016.06.30 How it works.
def how_it_works(request):
    return render(request, 'how_it_works.html')

# 2016.09.23 Privacy policy.
def privacy_policy(request):
    return render(request, 'privacy_policy.html')

def login(request):

    # Get URL parameter.
    isInvited = request.GET.get('Invitation', False)
    # 2016.08.12 League module.
    isSeasonRegistration = request.GET.get('SeasonRegistration', False)

    if isInvited:
        t_id = request.GET.get('Team')
        p_id = request.GET.get('Player')
    elif isSeasonRegistration:
        l_id = request.GET.get('League')
        s_id = request.GET.get('Season')

    if request.user.is_authenticated():
        if isInvited:
            return redirect('invite_registration', 
                            team_id=t_id, player_id=p_id)
        else:
            return redirect('myteams')

    if request.method == 'POST':
        username = request.POST.get('email', '').split('@')[0]
        password = request.POST.get('password', '')

        user = auth.authenticate(username=username, password=password)

        if user is not None and user.is_active:
            auth.login(request, user)
            if isInvited:
                return redirect('invite_registration', 
                                team_id=t_id, player_id=p_id)
            elif isSeasonRegistration:
                return redirect('season_registration', 
                                league_id=l_id, season_id=s_id)
            else:
                try:
                    team_id = Team.objects.filter(owners=request.user.id)[0].id
                except: # Without team.
                    team_id = None

                if team_id:
                    return HttpResponseRedirect('/teams/myteams/%s/summary' %team_id)
                else:
                    return HttpResponseRedirect('/teams/myteams/')
        else:
            if isInvited:
                # 2016.05.25 Message framework.
                messages.error(request, _('INCORRECT_EMAIL_OR_PASSWORD'))
                return render(request, 'login.html',
                              {'isInvited': isInvited, 'team_id': t_id,
                               'player_id': p_id})
            elif isSeasonRegistration:
                # 2016.08.12 League module.
                messages.error(request, _('INCORRECT_EMAIL_OR_PASSWORD'))
                return render(request, 'login.html',
                              {'isSeasonRegistration': isSeasonRegistration, 
                               'league_id': l_id, 'season_id': s_id})
            else:
                # 2016.05.25 Message framework.
                messages.error(request, _('INCORRECT_EMAIL_OR_PASSWORD'))
                return render(request, 'login.html')
    else: # request method = GET
        if isInvited:
            return render(request, 'login.html',
                          {'isInvited': isInvited, 'team_id': t_id,
                           'player_id': p_id})
        elif isSeasonRegistration:
            return render(request, 'login.html',
                          {'isSeasonRegistration': isSeasonRegistration, 
                           'league_id': l_id, 'season_id': s_id})
        else:
            return render(request, 'login.html')

def logout(request):
        try:
            auth.logout(request)
        except:
            # TODO: Log system.
            return 0
        return HttpResponseRedirect('/')

def register(request):

    # Get URL parameter.
    isInvited = request.GET.get('Invitation', False)
    # 2016.08.12 League module.
    isSeasonRegistration = request.GET.get('SeasonRegistration', False)

    if isInvited:
        t_id = request.GET.get('Team')
        p_id = request.GET.get('Player')
    elif isSeasonRegistration:
        l_id = request.GET.get('League')
        s_id = request.GET.get('Season')

    if request.method == 'POST':
        firstname = request.POST.get('firstname', '')
        lastname = request.POST.get('lastname', '')
        email = request.POST.get('email', '')
        username = email.split('@')[0]
        password = request.POST.get('password', '')

        # Create user.
        user = User.objects.create_user(username, email, password)
        user.first_name = firstname
        user.last_name = lastname
        user.save()

        # Authenticate user.
        auth_user = auth.authenticate(username=username, password=password)

        if auth_user is not None and auth_user.is_active:
            # Login user and redirect to My Teams.
            auth.login(request, auth_user)
            if isInvited:
                return redirect('invite_registration',
                                team_id=t_id, player_id=p_id)
            elif isSeasonRegistration:
                return redirect('season_registration_new',
                                league_id=l_id, season_id=s_id)
            else:
                return HttpResponseRedirect('/teams/myteams/')
        else:
            return redirect('index')
    if isInvited: 
        return render(request, 'register.html',
                      {'isInvited': isInvited, 'team_id': t_id,
                       'player_id': p_id})
    elif isSeasonRegistration:
        return render(request, 'register.html',
                      {'isSeasonRegistration': isSeasonRegistration,
                       'league_id': l_id, 'season_id': s_id})
    return render(request, 'register.html')

def my_account(request):
    if request.method == 'POST':
        user = User.objects.get(pk=request.user.id)
        firstname = request.POST.get('firstname', '')
        lastname = request.POST.get('lastname', '')

        print user.email

        try:
            user.first_name = firstname
            user.last_name = lastname
            user.save()
            # 2016.05.25 Message framework.
            messages.success(request, _('MY_ACCOUNT_UPDATED'))
        except:
            # TODO: Log system.
            # 2016.05.25 Message framework.
            messages.error(request, _('UNABLED_TO_UPDATE_MY_ACCOUNT'))
        
        return redirect('my_account')
    else:
        user = User.objects.get(pk=request.user.id)
        return render(request, 'my_account.html', locals())

def change_password(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if request.user.is_authenticated():
            try:
                user = User.objects.get(pk=request.user.id)
                user.set_password(password)
                user.save()
                # 2016.05.25 Message framework.
                messages.success(request, _('PASSWORD_UPDATED'))
            except:
                # TODO: Log system.
                # 2016.05.25 Message framework.
                messages.error(request, _('UNABLED_TO_CHANGE_PASSWORD'))
                return redirect('change_password')

        auth.logout(request)

        return HttpResponseRedirect('/accounts/login/')
    else:
        if request.user.is_authenticated():
            user = User.objects.get(pk=request.user.id)
            return render(request, 'change_password.html', locals())
        else:
            return render(request, 'login.html')
