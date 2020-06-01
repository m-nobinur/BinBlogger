from django.shortcuts import render, redirect
from django.views.generic import TemplateView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import ProfileUpdateForm, UserUpdateForm
from posts.models import Post
from comments.models import Comment, Reply

# profile update view
@login_required
def Profile_Update(request):
    
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST,
                                        request.FILES,
                                        instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            
            messages.success(request, 'Profile Updated')  
            return redirect('profile_update')
    
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    
    user = request.user
    user_posts = Post.objects.filter(author=user)
    comments_count = Comment.objects.filter(author=user).count()
    replies_count = Reply.objects.filter(author=user).count()
    comments_count = int(comments_count) + int(replies_count)
    post_counts = user_posts.count() 
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'post_counts':post_counts,
        'comments_count':comments_count,
    }
    
    return render(request, 'account/profile_update.html', context)
    

