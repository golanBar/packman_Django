from django.http import *
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

from packmanApp.models import Team, UserProfile

def loginUser(request):
    print("in loginUser")
    if request.POST:
        _username=request.POST['packmanApp_username']
        _password=request.POST['packmanApp_password']
        user = authenticate(username=_username, password=_password)
        if user is not None:
            # the password verified for the user
            if user.is_active:
                # User is valid, active and authenticated
                login(request, user)
                if UserProfile.objects.get(user=request.user).team:
                    # user has already joined a group
                    context = {'profile': UserProfile.objects.get(user=request.user), 'bestTeam': findBestTeam()}    
                    return render(request, 'packmanApp/showStatistics.html', context)
                else:                    
                    return HttpResponseRedirect('joinTeam/')
        else:
            _createNewUser = request.POST.get('createNewUser', False)
            if _createNewUser:# Checkbox was checked
                user = User.objects.create_user(_username, '', _password)#this saves the new user to the DB
                user = authenticate(username=_username, password=_password)#must successfully authenticate the user before calling login()
                login(request, user)
                return HttpResponseRedirect('joinTeam/')
            else:
                return render(request, 'packmanApp/login.html', {'error': True})
    return render(request, 'packmanApp/login.html')


def joinTeam(request):
    print("in joinTeam")
    TeamsList = Team.objects.order_by('name')[:5]
    context = {'TeamsList': TeamsList}
    return render(request, 'packmanApp/joinTeam.html', context)
    
def showStatistics(request):
    print("in showStatistics")  
    if request.POST.get("Join", False):
        selectedTeamName = request.POST.get('team', False)
        if selectedTeamName == False:
            print("no team selected")  
            TeamsList = Team.objects.order_by('name')[:5]
            context = {'TeamsList': TeamsList, 'error': True}
            return render(request, 'packmanApp/joinTeam.html', context)            
        else:
            selectedTeam = Team.objects.get(name__startswith=selectedTeamName) 
            #add the user to the selected team
            profile = UserProfile.objects.get(user=request.user)
            profile.team = selectedTeam
            profile.save()            
    #show the statistics
    context = {'profile': UserProfile.objects.get(user=request.user), 'bestTeam': findBestTeam()}    
    return render(request, 'packmanApp/showStatistics.html', context)

@csrf_exempt    
def persistScore(request): 
    print("in persistScore") 
    bodyUnicode = request.body.decode(encoding='UTF-8')
    newScore = int(bodyUnicode.split('&')[0].split('score=')[1])
    username = bodyUnicode.split('&')[1].split('username=')[1]   
                
    # update user's data
    profile = UserProfile.objects.get(user__username=username)
    if profile is not None:
        if profile.bestScore < newScore:
            profile.bestScore = newScore            
        profile.avgScore = ((profile.avgScore*profile.numGames)+newScore)/(profile.numGames+1)
        profile.numGames += 1
        profile.save()
    
    # update user's team's data
    if profile.team is not None:
        if profile.team.bestScore < newScore:
            profile.team.bestScore = newScore
        profile.team.avgScore = ((profile.team.avgScore*profile.team.numGames)+newScore)/(profile.team.numGames+1)
        profile.team.numGames += 1
        profile.team.save()        
    
    return(None)    
    
def findBestTeam():    
    bestTeam = None
    max = 0
    for team in Team.objects.all():
        if max<=team.bestScore:
            max = team.bestScore
            bestTeam = team
    return bestTeam
