from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import(View,
                                 DeleteView,
                                 )

from posts.models import Post, Category

from pages.tags_cats_gen import gen_tags

# global setup
def get_posts_cats_tags(req=None, tag_count=3, admin=True):

    cat_tup_list, tag_tup_list = [], []
    if admin:
        posts = Post.objects.all().order_by('-created_on')
        categories = list(set([cat for post in posts for cat in post.categories.all()]))
        tags = gen_tags(posts, tag_count)
        for cat in categories:
                user_post_count = cat.post_set.all().filter(author=req.user).count()
                cat_tup_list.append((cat, user_post_count))
        for tag in tags:
            tag_posts = Post.objects.filter(tags__icontains=tag).all()
            tag_tuple = (tag, len(tag_posts))
            tag_tup_list.append(tag_tuple)
    else:
        posts = Post.objects.filter(author=req.user).order_by('-created_on')
        categories = list(set([cat for post in posts for cat in post.categories.all()]))
        tags = gen_tags(posts, tag_count)
        for cat in categories:
            user_post_count = cat.post_set.all().filter(author=req.user).count()
            cat_tup_list.append((cat, user_post_count))
        for tag in tags:
            tag_posts = Post.objects.filter(tags__icontains=tag).all().filter(author=req.user)
            tag_tuple = (tag, len(tag_posts))
            tag_tup_list.append(tag_tuple)
        
    return posts, cat_tup_list, tag_tup_list

# view for admin Dashboard
class UserDashboard(LoginRequiredMixin, View):

    def get(self, request, *args, **kargs):
        posts, cat_tup_list, tag_tup_list = get_posts_cats_tags(request, tag_count=10, admin=False)
        context = {
            'posts': posts,
            'cat_tup_list': cat_tup_list,
            'tag_tup_list': tag_tup_list,
        }
        return render(request, 'user_dashboard/ud_index.html', context)

# post that will be deleted by it's author-view
class DeletePostbyAuthor(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'admin_dashboard/confirm-delete.html'
    success_url = '/mydashboard/'
    success_message = 'Deleted'

#  Selected categories's posts view
@login_required
def user_dashboard_filter_category_posts_view(request, pk):
    posts, cat_tup_list, tag_tup_list = get_posts_cats_tags(request, tag_count=15, admin=False)  
    category = get_object_or_404(Category, pk=pk)
    cat_posts = category.post_set.all().filter(author=request.user)

    context = {
        'posts': cat_posts,
        'category': category,
        'cat_tup_list': cat_tup_list,
        'tag_tup_list': tag_tup_list,
    }

    return render(request, 'user_dashboard/ud_index.html', context)

#  Selected tag's posts view
@login_required
def user_dashboard_filter_tag_posts_view(request, tag):
    posts, cat_tup_list, tag_tup_list = get_posts_cats_tags(request, tag_count=15, admin=False)  

    tag_filter_posts = Post.objects.filter(
        tags__icontains=tag).all().filter(author=request.user)
    context = {
        'posts': tag_filter_posts,
        'tag_tup_list': tag_tup_list,
        'cat_tup_list': cat_tup_list,
        'tag': tag,
    }

    return render(request, 'user_dashboard/ud_index.html', context)
