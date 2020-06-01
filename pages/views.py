from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Q
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.views.generic import( View,   
                                TemplateView, 
                                DeleteView,                            
                                )
                              
from posts.models import Post, Category
from comments.models import Comment, Reply

User = get_user_model()

# function for generating tags
def gen_tags(post_list, num=3):
    '''
    this fucntion will take a post list and return {num} amount tags. 
    takes two arguments: 1.post_list and 2.amount tags to generate
    '''
    all_tag_list = [ post.tags.split(',') for post in post_list ]
    tags = set([ tag.strip() for tags in all_tag_list for tag in tags ])
    
    if len(tags) >= num:    
        return list(tags)[:num]
    else: 
        return list(tags)
    

# function for generating top categories
def gen_top_categories(cat_list, num:int):
    '''
    this fucntion will take a categories list and returns only
    top {nums} amount categories(contining max posts) 

    takes two arguments: category_list and amount top categories to return
    '''
    top_categories = []
    sorted_category = sorted([len(category.post_set.all()) for category in cat_list])[::-1]
    top_three = sorted_category[:3]
    
    if num > 3:
        for category in cat_list:
            if len(category.post_set.all()) in sorted_category:
                top_categories.append(category)
            else:
                continue
        top_categories = top_categories[:num]
    else:
        for category in cat_list:
            # get top 3 categories by sorting post_set for each category
            if len(category.post_set.all()) in top_three:
                top_categories.append(category)
            else:
                continue 
        top_categories = top_categories[:3]    
    return top_categories

# view for index page and home page
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

# view for admin Dashboard home page
class UserDashboard(LoginRequiredMixin, View):
    
    def get(self, request, *args, **kargs):
        #  latest post will be deleted later 
        posts = Post.objects.filter(author=request.user).order_by('-created_on')
        
        categories = list(set([cat for post in posts for cat in post.categories.all()]))
        cat_tup_list=[]
        for cat in categories:
            user_post_count = cat.post_set.all().filter(author=request.user).count()
            cat_tup_list.append((cat, user_post_count))
        
        tags = gen_tags(posts, 10)
        tag_tup_list = []
        for tag in tags:
            tag_posts = Post.objects.filter(tags__icontains=tag).all().filter(author=request.user)
            tag_tuple = (tag, len(tag_posts))
            tag_tup_list.append(tag_tuple)

        context = {
                'posts':posts,
                'cat_tup_list':cat_tup_list,
                'tag_tup_list':tag_tup_list,
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
    
    categories = list(set([cat for post in posts for cat in post.categories.all()]))
    cat_tup_list=[]
    for cat in categories:
        user_post_count = cat.post_set.all().filter(author=request.user).count()
        cat_tup_list.append((cat, user_post_count))
    
    category = get_object_or_404(Category, pk= pk)
    cat_posts = category.post_set.all()

    tags = gen_tags(posts, 15)
    tag_tup_list = []
    for tag in tags:
        tag_posts = Post.objects.filter(tags__icontains=tag).all().filter(author=request.user)
        tag_tuple = (tag, len(tag_posts))
        tag_tup_list.append(tag_tuple)

    context = {
        'posts':cat_posts,
        'category':category,
        'cat_tup_list': cat_tup_list,
        'tag_tup_list': tag_tup_list,  
    }
    
    return render(request, 'user_dashboard/ud_index.html', context)

#  admin dashboard selected tag's posts view   
@login_required
def user_dashboard_filter_tag_posts_view(request, tag):
    posts = Post.objects.filter(author=request.user).order_by('-created_on')
    
    categories = list(set([cat for post in posts for cat in post.categories.all()]))
    cat_tup_list=[]
    for cat in categories:
        user_post_count = cat.post_set.all().filter(author=request.user).count()
        cat_tup_list.append((cat, user_post_count))
    
    tags = gen_tags(posts, 15)
    tag_tup_list = []
    for tag in tags:
        tag_posts = Post.objects.filter(tags__icontains=tag).all().filter(author=request.user)
        tag_tuple = (tag, len(tag_posts))
        tag_tup_list.append(tag_tuple)
    
    tag_filter_posts = Post.objects.filter(tags__icontains=tag).all().filter(author=request.user)
    context = {
        'posts':tag_filter_posts,
        'tag_tup_list':tag_tup_list,
        'cat_tup_list':cat_tup_list,
        'tag': tag,   
    }
    
    return render(request, 'user_dashboard/ud_index.html', context)
  

# view for about page/about.html
class AboutView(TemplateView):
    template_name = "about.html"


# view for contact page/contact.html
class ContactView(View):
    pass

