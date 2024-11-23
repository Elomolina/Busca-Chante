from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE ,related_name="user")
    phone_number = models.IntegerField()
    profile_pic = models.ImageField(upload_to="profile_pic", blank=True, null=True)