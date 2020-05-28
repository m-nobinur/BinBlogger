from django.contrib import admin

from .models import Comment, Reply

class ReplyInline(admin.TabularInline):
    model = Reply
    extra = 0

class CommentAdmin(admin.ModelAdmin):
    inlines = [
        ReplyInline,
    ]
    list_display = ('comment_content','author')

admin.site.register(Comment, CommentAdmin)