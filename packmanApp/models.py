from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Team(models.Model):
    name = models.CharField(max_length=200)
    bestScore = models.IntegerField(default=0)
    avgScore = models.IntegerField(default=0)
    numGames = models.IntegerField(default=0)
    def __str__(self):
        return self.name
		

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    bestScore = models.IntegerField(default=0)
    avgScore = models.IntegerField(default=0)
    numGames = models.IntegerField(default=0)
    team = models.ForeignKey(Team, null=True) 
    
    def __str__(self):  
          return "%s's UserProfile" % self.user
            
            
def createUserProfile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        

post_save.connect(createUserProfile, sender=User)
          