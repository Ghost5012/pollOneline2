from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *
class RegistrationForm(UserCreationForm):
    date_of_birth=forms.DateField(label='dob',help_text='required Format:YY-M-D')
    place_of_birth=forms.CharField(label='pob')
    class Meta:
        model=User
        fields=('first_name','last_name','date_of_birth','place_of_birth','username')

class CandidateForm(forms.Form):

    class Meta:
        model=Candidate
        fields=('nom','prenom','party')

class Vote(forms.Form):
    class Meta:
        model=Vote
        fields=('voter','party')