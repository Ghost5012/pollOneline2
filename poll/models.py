from django.db import models
from django.db.models.signals import post_save
from django import forms
from django.dispatch import receiver
from django.contrib.auth.models import User
#all our voters and administrators will be managed in the same table
class Electeur(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    #cni_number=models.IntegerField(primary_key=True)
    #here the cni_number will be used for username to 
    # help identify the user uniquely
    date_of_birth=models.DateField()
    palce_of_birth=models.CharField(max_length=15)
    picture=models.ImageField(upload_to="faces/")
    level=[("Agent","Agent"),("President","Surpeme court présidents"),("Voter","voter")]
    status=models.CharField(max_length=12,choices=level,default="Voter")
#the methods below specify that each time a new user is created,
#a voter(electeur) profile is assigned to him
@receiver(post_save,sender=User)
def create_electeur_profile(sender,instance,created, **kwargs):
    if created:
        Electeur.objects.create(user=instance)
@receiver(post_save,sender=User)
def save_electeur_profile(sender,instance,**kwargs):
    instance.electeur.save()

class Party(models.Model):
    p_name=models.CharField(max_length=45)
    p_acronyme=models.CharField(max_length=5)
    p_logo=models.ImageField(upload_to='logos/')

class Candidate(models.Model):
    nom=models.CharField(max_length=25)
    prenom=models.CharField(max_length=25)
    party=models.ForeignKey(Party,on_delete=models.CASCADE)

class Vote(models.Model):
    voter=models.ForeignKey(Electeur,on_delete=models.CASCADE)
    p_party=models.ForeignKey(Party,on_delete=models.CASCADE)