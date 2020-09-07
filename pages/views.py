from django.shortcuts import render
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.views.generic import(View,
                                 ListView,
                                 )

from posts.models import Post, Category
from comments.models import Comment, Reply
from contact.models import Message
from .tags_cats_gen import gen_tags, gen_top_categories

User = get_user_model()

class HomePageView(View):

    def get(self, request, *args, **kargs):
        
        #  latest post will be deleted later    
        latest_post = Post.objects.order_by('-created_on')[0:3]
        popular_post = Post.objects.order_by('-hit_count__hits')[:6]
        categories = Category.objects.all()
        
        posts = Post.objects.all()
        featured_posts = posts.filter(featured=True).order_by('-updated_on')
        if featured_posts:
            featured_post = featured_posts[0]
        else:
            if posts:
                featured_post = posts[len(posts)-1]
            else:
                featured_post = None

        top3_categories = gen_top_categories(categories, 3)
        tags = gen_tags(posts, 10)

        context = {
                'featured_post':featured_post,
                'latest_post':latest_post,
                'popular_post': popular_post,
                'top3_categories':top3_categories,
                'categories':categories,
                'tags':tags,
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

        posts = Post.objects.all()
        categories = Category.objects.all()
        latest_post = Post.objects.order_by('-created_on')[0:3]
        tags = gen_tags(posts, 10)
        top3_categories = gen_top_categories(categories, 3)
        
        context["latest_post"] = latest_post
        context["categories"] = categories
        context["tags"] = tags
        context["top3_categories"] = top3_categories

        return context
# authors page view
class AuthorPageView(View):
    
    def get(self, request, *args, **kargs):
        users = User.objects.all()
        authors = []
        for user in users:
            user_posts = Post.objects.filter(author=user)
            if user_posts.count() > 0 :
                comments_count = Comment.objects.filter(author=user).count()
                replies_count = Reply.objects.filter(author=user).count()
                comments_count = int(comments_count) + int(replies_count)
                post_counts = user_posts.count()
                authors.append((user, post_counts, comments_count ))
                
        context = {
            'authors': authors,
        }
        
        return render(request, 'pages/authors.html', context)
        

# search view for pages/search.html
class SearchView(View):
    def get(self, request, *args, **kargs):
        posts = Post.objects.all()
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

# search view for pages/search.html
class SearchView(View):
    def get(self, request, *args, **kargs):
        query = request.GET.get('q')
        posts = Post.objects.all().order_by('-created_on')
        # if query exists then filter posts by query
        if query:
            posts = posts.filter(Q(title__icontains=query) |
                                 Q(content__icontains=query)).distinct()

        context = {
            'page_obj': posts,
            'query': query,
        }

        return render(request, 'pages/search.html', context)

# view for contact page/contact.html
class ContactView(View):
    def get(self, request, *args, **kargs):
        return render(request, 'pages/contact.html')
    
    def post(self, request, *args, **kargs):
        name = request.POST.get('txtName', None)
        email = request.POST.get('txtEmail', None)
        phone = request.POST.get('txtPhone', None)
        massage = request.POST.get('txtMsg', None)

        contact = Message.objects.create(name=name,
                                        email= email,
                                        phone=phone,
                                        massage= massage,
                    )
        contact.save()
        messages.success(request, 'Your massage has been recorded.')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
       
