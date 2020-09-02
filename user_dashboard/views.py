from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import(View,
                                 DeleteView,
                                 )

from posts.models import Post, Category
from pages.tags_cats_gen import gen_tags

# view for admin Dashboard


class UserDashboard(LoginRequiredMixin, View):

    def get(self, request, *args, **kargs):
        #  latest post will be deleted later
        posts = Post.objects.filter(
            author=request.user).order_by('-created_on')

        categories = list(
            set([cat for post in posts for cat in post.categories.all()]))
        cat_tup_list = []
        for cat in categories:
            user_post_count = cat.post_set.all().filter(author=request.user).count()
            cat_tup_list.append((cat, user_post_count))

        tags = gen_tags(posts, 10)
        tag_tup_list = []
        for tag in tags:
            tag_posts = Post.objects.filter(
                tags__icontains=tag).all().filter(author=request.user)
            tag_tuple = (tag, len(tag_posts))
            tag_tup_list.append(tag_tuple)

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

#  admin dashboard selected categories's posts view


@login_required
def user_dashboard_filter_category_posts_view(request, pk):
    posts = Post.objects.filter(author=request.user).order_by('-created_on')

    categories = list(
        set([cat for post in posts for cat in post.categories.all()]))
    cat_tup_list = []
    for cat in categories:
        user_post_count = cat.post_set.all().filter(author=request.user).count()
        cat_tup_list.append((cat, user_post_count))

    category = get_object_or_404(Category, pk=pk)
    cat_posts = category.post_set.all()

    tags = gen_tags(posts, 15)
    tag_tup_list = []
    for tag in tags:
        tag_posts = Post.objects.filter(
            tags__icontains=tag).all().filter(author=request.user)
        tag_tuple = (tag, len(tag_posts))
        tag_tup_list.append(tag_tuple)

    context = {
        'posts': cat_posts,
        'category': category,
        'cat_tup_list': cat_tup_list,
        'tag_tup_list': tag_tup_list,
    }

    return render(request, 'user_dashboard/ud_index.html', context)

#  admin dashboard selected tag's posts view


@login_required
def user_dashboard_filter_tag_posts_view(request, tag):
    posts = Post.objects.filter(author=request.user).order_by('-created_on')

    categories = list(
        set([cat for post in posts for cat in post.categories.all()]))
    cat_tup_list = []
    for cat in categories:
        user_post_count = cat.post_set.all().filter(author=request.user).count()
        cat_tup_list.append((cat, user_post_count))

    tags = gen_tags(posts, 15)
    tag_tup_list = []
    for tag in tags:
        tag_posts = Post.objects.filter(
            tags__icontains=tag).all().filter(author=request.user)
        tag_tuple = (tag, len(tag_posts))
        tag_tup_list.append(tag_tuple)

    tag_filter_posts = Post.objects.filter(
        tags__icontains=tag).all().filter(author=request.user)
    context = {
        'posts': tag_filter_posts,
        'tag_tup_list': tag_tup_list,
        'cat_tup_list': cat_tup_list,
        'tag': tag,
    }

    return render(request, 'user_dashboard/ud_index.html', context)
