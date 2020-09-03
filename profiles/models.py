from django.db import models
from django.contrib.auth import get_user_model

from PIL import Image
from django_resized import ResizedImageField

User = get_user_model()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    image = ResizedImageField(size=[300, 300], crop=['middle', 'center'], quality=85, keep_meta=False, verbose_name='profile_pic', default ='default.jpg', upload_to='profile_pics', force_format='JPEG')
    bio = models.CharField(max_length = 280, blank =True)
    about = models.TextField(verbose_name='about')

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
             
    # delete profile img too
    def delete(self, *args, **kwargs):
        self.image.delete()
        
        return super(Profile, self).delete(*args, **kwargs)