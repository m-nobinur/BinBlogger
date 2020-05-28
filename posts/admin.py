from django.contrib import admin

from django_summernote.admin import SummernoteModelAdmin

from .models import Category, Post
from comments.models import Comment

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
 
class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',) 
    inlines = [
        CommentInline,
    ]
    list_display = ('title','author')  
    
 
# Register your models here.
admin.site.register(Post,PostAdmin)
admin.site.register(Category)