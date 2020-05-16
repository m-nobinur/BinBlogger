from django.db import models
from django.contrib.auth import get_user_model
from PIL import Image


User = get_user_model()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(verbose_name='profile_pic', default ='default.jpg', upload_to='profile_pics')
    bio = models.CharField(max_length = 280, blank =True)
    about = models.TextField(verbose_name='about')

    def __str__(self):
        return f'{self.user.first_name} || {self.user.username}'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)