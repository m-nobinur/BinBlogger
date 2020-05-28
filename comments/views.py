from django.shortcuts import redirect, reverse, get_object_or_404
from .models import Comment, Reply
from posts.models import Post

# add comment view
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post_comment = request.POST['post-comment']
        comment = Comment.objects.create(author=request.user, 
                                         post= post,
                                         comment_content=post_comment,)
        comment.save()                                         
        return redirect(reverse('post-detail', kwargs={
            'pk': pk
        }))
    else:
        return redirect('home')
        
# add reply to comment view
def reply_comment(request, ppk, cpk):
    comment = get_object_or_404(Comment, pk=cpk)
    if request.method == 'POST':
        reply_content = request.POST.get('reply_content', None)
        reply = Reply.objects.create(author=request.user, 
                                         comment = comment,
                                         reply_content=reply_content,)
        reply.save()                                         
        return redirect(reverse('post-detail', kwargs={
            'pk': ppk
        }))
    else:
        return redirect('home')
        
