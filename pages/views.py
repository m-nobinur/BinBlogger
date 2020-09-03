from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.views.generic import(View,
                                 TemplateView,
                                 ListView,
                                 )

from posts.models import Post, Category
from comments.models import Comment, Reply
from pages.tags_cats_gen import gen_tags, gen_top_categories

# ---------- global setup start ---------
User = get_user_model()

users = User.objects.all()
posts = Post.objects.all()
latest_post = Post.objects.order_by('-created_on')[0:3]
popular_post = Post.objects.order_by('-hit_count__hits')[:6]
categories = Category.objects.all()
top3_categories = gen_top_categories(categories, 3)
tags = gen_tags(posts, 10)
# ---------- global setup end ---------

class HomePageView(View):

    def get(self, request, *args, **kargs):
        global posts
        featured_posts = posts.filter(featured=True).order_by('-updated_on')
        if featured_posts:
            featured_post = featured_posts[0]
        else:
            if posts:
                featured_post = posts[len(posts)-1]
            else:
                featured_post = None

        context = {
            'featured_post': featured_post,
            'latest_post': latest_post,
            'popular_post': popular_post,
            'top3_categories': top3_categories,
            'categories': categories,
            'tags': tags,
        }

        return render(request, 'pages/home.html', context)


# view for blog/blog.html
class BlogPageView(ListView):

    model = Post
    template_name = 'blog/blog.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["latest_post"] = latest_post
        context["categories"] = categories
        context["tags"] = tags
        context["top3_categories"] = top3_categories

        return context

# authors page view
class AuthorPageView(View):

    def get(self, request, *args, **kargs):
        
        authors = []
        for user in users:
            user_posts = Post.objects.filter(author=user)
            if user_posts.count() > 0:
                comments_count = Comment.objects.filter(author=user).count()
                replies_count = Reply.objects.filter(author=user).count()
                comments_count = int(comments_count) + int(replies_count)
                post_counts = user_posts.count()
                authors.append((user, post_counts, comments_count))

        context = {
            'authors': authors,
        }

        return render(request, 'pages/authors.html', context)


# search view for pages/search.html
class SearchView(View):
    def get(self, request, *args, **kargs):
        global posts
        query = request.GET.get('q')

        # if query exists then filter posts by query
        if query:
            posts = posts.filter(Q(title__icontains=query) |
                                 Q(content__icontains=query)).distinct()

        context = {
            'page_obj': posts,
            'query': query,
        }

        return render(request, 'pages/search.html', context)

# view for about page/about.html
class AboutView(TemplateView):
    template_name = "about.html"

# view for contact page/contact.html
class ContactView(View):
    pass
