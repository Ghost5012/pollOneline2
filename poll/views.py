from django.shortcuts import render, redirect
import json
import random
from highcharts.views import HighChartsBarView
from django.db.models import Count, Q
from django.contrib.auth.hashers import make_password,check_password
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views import View
from django.contrib.auth import authenticate, login,urls, logout
from .forms import *
from .fusioncharts.fusioncharts import FusionCharts
import os
from face_detection.views import detect
from poll.models import *
# Create your views here.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import datetime

#------*---*-- Take note of the line below
eldate=datetime.date(2018,11,11)
#------*--*--- to set the current as the election day,uncomment the line below and comment the one up
#eldate=datetime.date.today()

class IndexView(View):
    """vue présentant la page d'acceuil site de vote"""
    def get(self,request):
        party=Party.objects.order_by('pk')
        context={'party':party}
        return render(request,'poll/index.html',context)

def AdPicture(request):
    """requis pour ajouter la photo dun utilisateur au profil actuel"""
    userId=request.session['userId']
    request.session['userId']
    request.session['userId']=userId
    picture=BASE_DIR+'/ml/dataset/'+str(id)+'.'+str(1)+'.jpg'
    request.session['picture']=picture
    context={'picture':picture,'form':RegistrationForm()}
    return render(request,'poll/homeAdmin1.html',context)

class LoginView(View):
    """this view checks user informations and sends the user to the 
    appropriate destination according to the current date"""
    def post(self,request):
        username=request.POST['nom']
        password=request.POST['pw']
        user=authenticate(request,username=username,password=password)
        if user is not None:
            if eldate==datetime.date.today():
                if user.electeur in [p.voter for p in Vote.objects.all()]:
                    login(request,user)
                    return redirect('poll:chart')
                else:
                    face=detect(request,user.username)
                    if face:
                        party=Party.objects.order_by('pk')
                        context={'party':party}
                        login(request,user)
                        return render(request,'poll/vote.html',context)
                    else:
                        return redirect('poll:index')
            else:
                """each user should be sent to the appropriate direction"""
                if user.electeur.status=="Agent":
                    """the agents"""
                    form=RegistrationForm()
                    login(request,user)
                    return render(request,'poll/homeAdmin1.html')
                elif user.electeur.status=="President":
                    """the president of the supreme court"""
                    login(request,user)
                    return render(request,'poll/superAdmin.html',{'form':RegistrationForm()})
                else:
                    """the voters"""
                    login(request,user)
                    return render(request,'poll/homeVoter.html')
                    
        else:
            """the user is not defined"""
            return redirect('poll:index')

class LogoutView(View):
    def get(self,request):
        logout(request)
        return redirect('poll:index')
 
class RegisterElecteur(View):
    """called to save the Voter"""
    def post(self,request):
        satut=''
        """here we should know the tipe of user we are saving"""
        if request.user.electeur.status=="Agent":
            satut="Voter"
        else:
            satut="Agent"
        try:
            u=str(request.session['userId'])
            name=request.POST['name']
            surname=request.POST['surname']
            dob=request.POST['dob']
            pob=request.POST['pob']
            us=User.objects.create(username=u,first_name=name,last_name=surname,password=make_password(u))
            us.electeur.date_of_birth=dob
            us.electeur.place_of_birth=pob
            #us.electeur.picture=BASE_DIR+'ml/dataset'+u+".1.jpg"
            us.save()
            return render(request,'poll/homeAdmin1.html')
        except:
           return render(request,'poll/homeAdmin1.html',{'error':"Error, fill the form and try again"})
            

class RegAgents(View):
    def get(self,request):

        return render(request,'poll/regAgents.html',{'form':RegistrationForm()})

class SaveParty(View):
    """cette vue enregistre les parties politiques dans la base de données"""
    def post(self,request):
        pname=request.POST['party']
        pacronyme=request.POST['acronym']
        logo=request.POST['logo']
        party=Party(p_name=pname,p_acronyme=pacronyme,p_logo=logo)
        party.save()
        return render(request,'poll/superAdmin.html')

class RegParty(View):
    """vue chargée de retourner la page d'enregistrement des parties politiques"""
    def get(self,request):
        return render(request,'poll/regParty.html')
class RegCandidates(View):
    def get(self,request):
        party=Party.objects.order_by('pk')
        context={'party':party}
        return render(request,'poll/regCandidates.html',context)

class SaveCandidates(View):
    """cette vue enregistre les parties politiques dans la base de données"""
    def post(self,request):
        name=request.POST['nom']
        sname=request.POST['surname']
        pname=request.POST['party']
        party=Party.objects.get(p_acronyme=pname)
        candidate=Candidate(nom=name,prenom=sname,party=party)
        candidate.save()
        return render(request,'poll/superAdmin.html')

class Votes(View):
    def post(self,request):
        electeur=request.user
        choix=request.POST['party']
        party=Party.objects.get(p_acronyme=choix)
        vote=Vote(voter=electeur.electeur,p_party=party)
        vote.save()
        return redirect('poll:index')

class Change_password(View):
    def post(self,request):
        ppw=request.POST['prev']
        npw=request.POST['new']
        if request.user.check_password(ppw):
            if len(str(npw))<8:
                err="Your password should be at least 8 characters long"
                return render(request,'poll/changePassword.html',{'error':err})
            else:
                request.user.set_password(npw)
                request.user.save()
                return redirect('poll:logout')
        else:
            err="The previous password didn't match, try again"
            return render(request,'poll/changePassword.html',{'error':err})

class PassWord(View):
    def get(selt,request):
        return render(request,'poll/changePassword.html')

class Result(HighChartsBarView):
    categories=list()
    for p in Party.objects.all():
        categories.append(p.p_acronyme)
    @property
    def series(self):
        result=list()
        for name in ('joe','jack','William','averell'):
            data=list()
            for x in range(len(self.categories)):
                data.append(random.randint(0,10))
            result.append({'name':name,"data":data})
        return render('poll/chart.html',{'result':json.dumps(result)})
"""def chart(request):
    dataset=list()
    abst=Vote.objects.count()
    for p in Party.objects.all():
        d=dict()
        d['party']=p.p_acronyme
        c=0
        for v in Vote.objects.all():
           if v.p_party is p:
               c+=1
        d['v']=(c/abst)*100
        dataset.append(d)
    parties=list()
    voix=list()
    for entry in dataset:
        parties.append(entry['party'])
        voix.append(entry['v'])
    return render (request,'poll/chart.html',
    {'categories':json.dumps(parties),
    'voix':json.dumps(voix)})"""

def test(request):
    return render(request,'poll/chart.html')