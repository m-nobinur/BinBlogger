from django.contrib import admin

from .models import Message

class MessageAdmin(admin.ModelAdmin):

    list_display = ('name', 'email', 'phone', 'massage')
    search_fields = ['email']
    
admin.site.register(Message, MessageAdmin)
