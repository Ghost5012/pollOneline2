from django.urls import path, include
from poll.views import *
app_name='poll'
urlpatterns=[path('',IndexView.as_view(),name='index'),
path('login/',LoginView.as_view(),name='login'),
path('home',RegisterElecteur.as_view(),name='regVoter'),
path('logout',LogoutView.as_view(),name='logout'),
path('admin',AdPicture,name='ap'),
path('home/register agents/',RegAgents.as_view(),name='regAgents'),
path('regparty',RegParty.as_view(),name='regParty'),
path('home/save party/',SaveParty.as_view(),name="saveParty"),
path('home/register candidate',RegCandidates.as_view(),name='regCand'),
path('home/save candidate',SaveCandidates.as_view(),name='saveCand'),
path('vote/',Votes.as_view(),name="vote"),
path('home/password/',PassWord.as_view(),name="pw"),
path('change/',Change_password.as_view(),name='chPW')
]