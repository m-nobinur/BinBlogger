from django.db import models

class NewsleterAccount(models.Model):
    email = models.EmailField()
    sign_time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.email
    
    
