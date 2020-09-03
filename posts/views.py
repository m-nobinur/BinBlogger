from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView,
    View,
)

from hitcount.views import HitCountDetailView

from comments.models import Comment, Reply
from .models import Category, Post
from pages.views import (
    User, posts,
    latest_posts, popular_posts, 
    categories
)

# pagination
def paginate(req, page_num=5):
    paginator = Paginator(posts, page_num) 
    page_number = req.GET.get('page')
    return paginator.get_page(page_number)

# view for blog/add_post.html
class PostCreateView(LoginRequiredMixin, CreateView):

    model = Post
    template_name = "blog/add_post.html"
    fields = ['title', 'post_thumbnail', 'tags',
              'content', 'categories',
              'featured',
              ]
    success_url = '/blog'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

# view for blog/update_post.html
class PostUpdateView(SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, UpdateView):

    model = Post
    template_name = "blog/update_post.html"
    fields = ['title', 'post_thumbnail', 'tags',
              'content', 'categories', 'featured',
              ]

    success_message = 'Post Updated'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author or self.request.user.is_superuser:
            return True
        return False

class PostDeleteView(SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/blog'
    success_message = 'Post Deleted'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author or self.request.user.is_superuser:
            return True
        return False

# view for blog/post_details.html
class PostDetailView(HitCountDetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    count_hit = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        this_post = Post.objects.filter(id=self.object.id)
        tags = [tag.strip() for tag in this_post[0].tags.split(',')]

        context["latest_posts"] = latest_posts
        context["popular_posts"] = popular_posts
        context["tags"] = tags

        return context


# view for blog/user_posts.html
def UserPostsView(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user).order_by('-created_on')
    page_obj = paginate(request, page_num=8)
    posts_count = posts.count()
    comments_count = Comment.objects.filter(author=user).count()
    replies_count = Reply.objects.filter(author=user).count()
    total_user_comments = int(comments_count) + int(replies_count)

    context = {
        'author_user': user,
        'posts_count': posts_count,
        'comments_count': total_user_comments,
        'page_obj': page_obj,
    }

    return render(request, 'blog/user_posts.html', context)


# view for blog/posts_in_category.html
def Posts_in_CategoryView(request, id):

    category = get_object_or_404(Category, id=id)
    posts_in_cat = category.post_set.all()
    page_obj = paginate(request, page_num=8)

    context = {
        'posts_in_cat': posts_in_cat,
        'cat_name': category,
        'page_obj': page_obj,
    }

    return render(request, 'blog/posts_in_category.html', context)

# this view will add a category if it doesn't exist
class AddCategoryView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        category = request.POST['category']
        for_not_admin_view = request.POST.get('add_category', 'not_admin')

        if category and category.lower() not in [cat.category.lower() for cat in categories]:
            cat = Category.objects.create(category=category)
            cat.save()
            messages.success(request, f'{category} added as Category')
            if for_not_admin_view == 'add_post_view':
                return redirect('add_post')
            else:
                return redirect('admin-dashboard')
        else:
            messages.error(request, f'{category} is already a Category')
            return redirect('admin-dashboard')

# view for blog/tag_posts.html
def TagPostsView(request, tag):

    posts_in_tag = Post.objects.filter(tags__icontains=tag).all()
    page_obj = paginate(request, page_num=7)

    context = {
        'posts_in_tag': posts_in_tag,
        'page_obj': page_obj,
        'tag_name': tag,
    }

    return render(request, 'blog/tag_posts.html', context)
