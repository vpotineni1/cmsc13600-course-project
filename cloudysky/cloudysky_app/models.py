from django.db import models
from django.contrib.auth.models import User as DjangoUser


# Create your models here.

class Role(models.Model):
    role_id = models.AutoField(primary_key=True)
    role_type = models.CharField(max_length=15)

class User(models.Model):
    user = models.OneToOneField(DjangoUser, on_delete= models.CASCADE, primary_key= True)
    role = models.ForeignKey(Role, on_delete= models.CASCADE)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    bio = models.TextField()
    username = models.CharField(max_length = 20)

class Media(models.Model):
    media_id = models.AutoField(primary_key=True)
    images = models.ImageField(upload_to="images/")
    title = models.CharField(max_length=50)
    content_text = models.TextField()

class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    content_id = models.ForeignKey(Media, on_delete = models.CASCADE)
    creator = models.ForeignKey(User, on_delete= models.CASCADE)
    censored = models.BooleanField(default= False)
    censored_reason = models.TextField(blank=True, null=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    add_time = models.DateTimeField(auto_now_add=True)


class Comments(models.Model):
    comment_id = models.AutoField(primary_key=True)
    creator = models.ForeignKey(User, on_delete= models.CASCADE)
    censored = models.BooleanField(default= False)
    censored_reason = models.TextField(blank=True, null=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    add_time = models.DateTimeField(auto_now_add=True)
    comment_content = models.TextField()
    post_id = models.ForeignKey(Post, on_delete = models.CASCADE)
    