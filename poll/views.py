from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.contrib.auth import authenticate, login,urls, logout
from .forms import *
import os
from face_detection.views import detect
from poll.models import *
# Create your views here.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import datetime
eldate=datetime.date(2018,6,10)
class IndexView(View):
    """vue présentant la page d'acceuil site de vote"""
    def get(self,request):
        party=Party.objects.order_by('pk')
        context={'party':party}
        return render(request,'poll/index.html',context)

def AdPicture(request):
    """requis pour ajouter la photo dun utilisateur au profil actuel"""
    userId=request.session['userId']
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
                """this is the election day"""
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
                    return render(request,'poll/homeAdmin1.html',{'form':form})
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
        form=RegistrationForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.refresh_from_db()
            user.electeur.date_of_birth=form.clean_data.get('date_of_birth')
            user.electeur.place_of_birth=form.clean_data.get('place_of_birth')
            user.electeur.status=satut
            user.electeur.picture=request.session['picture']
            user.save()
            form=RegistrationForm()
            return render(request,'poll/homeAdmin1.html',{'form':form})
            #return redirect()
        else:
            form=RegistrationForm()
            return render(request,'poll/homeAdmin1.html',{'form':form})

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