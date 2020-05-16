from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.shortcuts import redirect, reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin,LoginRequiredMixin
from django.views.generic import ( ListView,    
                                   DetailView,
                                   CreateView,
                                   UpdateView,
                                   DeleteView,
                                   )

from hitcount.views import HitCountDetailView

from .models import Category, Post
from .forms import PostForm
from pages.views import gen_tags


User = get_user_model()

# view for blog/blog.html
class BlogPageView(ListView):

    model = Post
    template_name = 'blog/blog.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        posts = Post.objects.all()
        categories = Category.objects.all()
        latest_post = Post.objects.order_by('-created_on')[0:3]
        tags = gen_tags(posts, 10)

        context["latest_post"] = latest_post
        context["categories"] = categories
        context["tags"] = tags

        return context
    
# view for blog/add_post.html
class PostCreateView(LoginRequiredMixin, CreateView):
    
    model = Post
    template_name = "blog/add_post.html"
    fields = [ 'title', 'post_thumbnail', 'tags', 
                  'content', 'categories',
                  'status', 'featured',
                 ]
    success_url = '/blog'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


# view for blog/update_post.html
class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    
    model = Post
    template_name = "blog/update_post.html"
    fields = [ 'title', 'post_thumbnail', 'tags', 
                  'content', 'categories', 'featured',
                 ]
    success_url = '/blog'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author or self.request.user.is_superuser:
            return True
        return False

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/blog'
    
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
        latest_posts = Post.objects.order_by('-created_on')[0:3]
        popular_posts = Post.objects.order_by('-hit_count__hits')[:3]
        tags = this_post[0].tags.split()

        context["latest_posts"] = latest_posts
        context["popular_posts"] = popular_posts
        context["tags"] = tags

        return context


# view for blog/user_posts.html
def UserPostsView(request, username):
    user = get_object_or_404(User, username= username)
    posts = Post.objects.filter(author=user).order_by('-created_on')
    
    # pagination
    paginator = Paginator(posts, 8) # Show 8 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'author_user': user,
        'page_obj': page_obj,
    }

    return render(request, 'blog/user_posts.html', context)


# view for blog/posts_in_category.html
def Posts_in_CategoryView(request, id):
    
    category = get_object_or_404(Category, id = id)
    posts_in_cat = category.post_set.all()

    # pagination
    paginator = Paginator(posts_in_cat, 8) # Show 4 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
            'posts_in_cat':posts_in_cat,
            'cat_name': category,
            'page_obj': page_obj,
    }

    return render(request, 'blog/posts_in_category.html', context)


# view for blog/tag_posts.html
def TagPostsView(request, tag):

    posts_in_tag = Post.objects.filter(tags__icontains=tag).all()

    # pagination
    paginator = Paginator(posts_in_tag, 7) # Show 4 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
            'posts_in_tag':posts_in_tag,
            'page_obj': page_obj,
            'tag_name': tag,
    }

    return render(request, 'blog/tag_posts.html', context)


