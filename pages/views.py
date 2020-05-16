from django.shortcuts import render
from django.db.models import Count, Q
from django.views.generic import( View,   
                                TemplateView,                             
                                )
                              
from posts.models import Post, Category


# function for generating tags
def gen_tags(post_list, num):
    '''
    this fucntion will take a post list and return {num} amount tags
    takes two arguments: post_list and amount top tags to return
    '''

    all_tag_list = [ post.tags.split() for post in post_list ]
    tags = set([ tag for tags in all_tag_list for tag in tags ])

    return list(tags)[:num]

# function for generating top categories
def gen_top_categories(cat_list, num):
    '''
    this fucntion will take a categories list and return only 
    top {nums} amount categories contining max posts 

    takes two arguments: category_list and amount top categories to return
    '''

    top_categories = []
    for category in cat_list:
        # get top 3 categories by sorting post_set for each category
        if len(category.post_set.all()) in sorted([len(category.post_set.all())][-num:]):
            top_categories.append(category)

    return top_categories


# view for index page and home page
class HomePageView(View):

    def get(self, request, *args, **kargs):
        featured_posts = Post.objects.filter(featured=True).order_by('-created_on')

        if featured_posts:
            featured_post = featured_posts[0]

        #  latest post will be deleted later    
        latest_post = Post.objects.order_by('-created_on')[0:3]
        popular_post = Post.objects.order_by('-hit_count__hits')[:6]
        posts = Post.objects.all()
        categories = Category.objects.all()

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


# view for about page/about.html
class AboutView(TemplateView):
    template_name = "about.html"


# view for contact page/contact.html
class ContactView(View):
    pass

