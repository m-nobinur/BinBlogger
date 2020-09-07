from django.db import models

class Message(models.Model):
    name = models.CharField(max_length=40)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=15)
    massage = models.TextField()

    def __str__(self):
        return self.massage[:60]