
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='userimg/', blank=True, null=True)
    address_line1 = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.CharField(max_length=10)
    


class Patient(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)

class Doctor(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)

class BlogPost(models.Model):
    CATEGORY_CHOICES = [
        ('Mental Health', 'MENTAL HEALTH'),
        ('Heart Disease', 'HEART DISEASE'),
        ('Covid19', 'COVID19'),
        ('Immunization', 'IMMUNIZATION'),
    ]
    
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='blog_images/',blank=True, null=True)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    summary = models.TextField()
    content = models.TextField()
    draft = models.BooleanField(default=True)

    def __str__(self):
        return self.title