from django.db import models
from django.contrib.auth.models import User

class Faculty(models.Model):
    faculty_name = models.CharField(max_length=255)

    def __str__(self):
        return self.faculty_name

class UserProfile(models.Model):
    avatar = models.ImageField(default='accounts/user_default.jpg', upload_to='accounts/') # Picture of user
    user = models.OneToOneField(User, on_delete=models.CASCADE) # reference to User Table
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE) # reference to Faculty Table

    def __str__(self):
        return self.user.username
    
class Badge(models.Model):
    name = models.CharField(max_length=255)
    points_required = models.IntegerField()
    image = models.ImageField(upload_to='badges/')

    def __str__(self):
        return self.name
    
class Reward(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    badges = models.ManyToManyField(Badge, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.points} points"