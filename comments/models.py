from django.db import models
from django.contrib.auth import get_user_model

from posts.models import Post

User = get_user_model()

# models for comment of post
class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_author')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    comment_time = models.DateTimeField(auto_now_add=True)
    comment_content = models.TextField()
    
    def __str__(self):
        return self.comment_content[:80]
    
    @property
    def get_all_reply(self):
        return self.replies.all().order_by('reply_time')
   
    @property
    def get_replies_count(self):
        return self.replies.all().count()

# models for comment of post
class Reply(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reply_author')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
    reply_time = models.DateTimeField(auto_now_add=True)
    reply_content = models.TextField()
    
    class Meta:
        verbose_name_plural = 'replies'
    
    def __str__(self):
        return self.reply_content[:80]