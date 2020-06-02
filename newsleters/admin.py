from django.contrib import admin

from .models import NewsleterAccount

class NewsleterAdmin(admin.ModelAdmin):

    list_display = ('email', 'sign_time')
    search_fields = ['email']
    
admin.site.register(NewsleterAccount, NewsleterAdmin)
    