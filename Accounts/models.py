from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class UserImage(models.Model):
    profileImage = models.ImageField(upload_to='user_images/', null=True, blank=True)
    backgroundImage = models.ImageField(upload_to='user_images/', null=True, blank=True)
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='userimage')

    def get_latest_profile_image_url(self):
        # Check if profileImage is set and return its URL
        if self.profileImage:
            return self.profileImage.url
        else:
            return None
 
    def get_latest_background_image_url(self):
        if self.backgroundImage:
            return self.backgroundImage.url 
        else:
            return None
    
class CustomUser(AbstractUser):
    nickname = models.CharField(max_length=50, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    school = models.CharField(max_length=100, blank=True)
    work = models.CharField(max_length=100, blank=True)
    living_at = models.CharField(max_length=100, blank=True)
    born_at = models.CharField(max_length=100, blank=True)

    #Future implementations:
    #friends = models.ManyToManyField('self', blank=True)
    #friend_count = models.IntegerField(default=0)
    
class Card(models.Model):
    image = models.ImageField(upload_to='card_images/', null=True, blank=True)  
    text = models.TextField()  
    recommended_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='recommended_cards')
    recommended_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)  
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owned_cards')

    def __str__(self):
        return f"Card (ID: {self.id}) - {self.text[:20]}"  
    
    class Meta:
        ordering = ['-created_at']



    