from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, DeleteView, ListView, UpdateView
from django.contrib.auth.mixins import UserPassesTestMixin,LoginRequiredMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import get_user_model

from posts.models import Post, Category
from pages.views import gen_tags


User = get_user_model()

# view for admin Dashboard home page
class AdminDbView(LoginRequiredMixin, UserPassesTestMixin, View):

    def test_func(self):
        if self.request.user.is_superuser:
             return True
        return False
    
    def get(self, request, *args, **kargs):

        #  latest post will be deleted later
        users = User.objects.all().order_by('date_joined')
        admins = users.filter(is_superuser=True).order_by('date_joined')
        lead_admin = admins[0]    
        posts = Post.objects.all().order_by('-created_on')
        featured_post = Post.objects.filter(featured=True).order_by('-updated_on')[0]
        categories = Category.objects.all()[:10]
        tags = gen_tags(posts, 15)
        
        
        tag_tup_list = []
        for tag in tags:
            tag_postscount = Post.objects.filter(tags__icontains=tag).all()
            tag_tuple = (tag, len(tag_postscount))
            tag_tup_list.append(tag_tuple)

        context = {
                'users':users,
                'posts':posts,
                'categories':categories,
                'tag_tup_list':tag_tup_list,
                'featured_post':featured_post,
                'lead_admin':lead_admin,
        }

        return render(request, 'admin_dashboard/admin_site.html', context)
  
#  admin dashboard all categories view   
class ADashAllCategoryView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Category
    template_name = "admin_dashboard/admin_posts_cats_tags_users.html"
    context_object_name = 'categories'
 
    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False

#  admin dashboard all tags view   
class ADashAllTagView(LoginRequiredMixin, UserPassesTestMixin, View):

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False
    
    def get(self, request, *args, **kargs):
        posts = Post.objects.all()
        tags = gen_tags(posts, len(posts)*4)
        
        tag_tup_list = []
        for tag in tags:
            tag_postscount = Post.objects.filter(tags__icontains=tag).all()
            tag_tuple = (tag, len(tag_postscount))
            tag_tup_list.append(tag_tuple)
        
        context = {
            'tag_tup_list': tag_tup_list,
        }
        return render(request, 'admin_dashboard/admin_posts_cats_tags_users.html', context)
    
 
 #  admin dashboard all user view   
class ADashAllUserView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User
    template_name = "admin_dashboard/admin_posts_cats_tags_users.html"
    context_object_name = 'users'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        all_users = User.objects.all().order_by('date_joined')
        admins = all_users.filter(is_superuser=True).order_by('date_joined')
        lead_admin = admins[0]
        
        context["lead_admin"] = lead_admin
        return context
         
    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False
     
#  admin dashboard all posts view   
class ADashAllPostsView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Post
    template_name = "admin_dashboard/admin_posts_cats_tags_users.html"
    context_object_name = 'posts'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        featured_post = Post.objects.filter(featured=True).order_by('-updated_on')[0]
        context["featured_post"] = featured_post
        return context
    
    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False
      
# post that will be deleted from admin dashboard -view
class DeletePostbyAdminView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'admin_dashboard/confirm-delete.html'
    success_url = '/binblogger-admin/dashboard/'
    
    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False


# category that will be deleted from admin dashboard - view
class DeleteCategorybyAdmin(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Category
    template_name = 'admin_dashboard/confirm-delete.html'
    success_url = '/binblogger-admin/dashboard/'
    
    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False

# category update view on admin dashboard - view
class UpdateCategorybyAdmin(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Category
    fields = ['category']
    template_name = 'admin_dashboard/update-category.html'
    success_url = '/binblogger-admin/dashboard/'
    
    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False
 

# super user check fucntion for restricting user -funtion for @user_passes_test decorator
def super_user_check(user):
    if user.is_superuser:
        return True   
    else:
        return False  

# admin's power to make a post to featured post
@login_required
@user_passes_test(super_user_check)
def make_the_post_featured(request, pk):
    post = get_object_or_404(Post, pk= pk)
    if post:
        post.featured = True
        post.save()
        return redirect('admim-dashboard')

 #  admin dashboard selected categories's posts view   
@login_required
@user_passes_test(super_user_check)
def admin_dashboard_filter_category_posts_view(request, pk):
    all_posts = Post.objects.all()
    tags = gen_tags(all_posts, 15)
    users = User.objects.all().order_by('date_joined')
    categories = Category.objects.all()[:10]
    category = get_object_or_404(Category, pk= pk)
    cat_posts = category.post_set.all()
    if len(cat_posts) > 0:
        posts = cat_posts
        featured_post = posts.filter(featured=True).order_by('-updated_on')[0]
    else:
        posts = None
        featured_post = None
    
    tag_tup_list = []
    for tag in tags:
        tag_postscount = Post.objects.filter(tags__icontains=tag).all()
        tag_tuple = (tag, len(tag_postscount))
        tag_tup_list.append(tag_tuple)
    
    context = {
        'posts':posts,
        'featured_post':featured_post, 
        'category':category,
        'users': users,
        'categories':categories,
        'tag_tup_list': tag_tup_list,  
    }
    
    return render(request, 'admin_dashboard/admin_site.html', context)

#  admin dashboard selected tag's posts view   
@login_required
@user_passes_test(super_user_check)
def admin_dashboard_filter_tag_posts_view(request, tag):
    all_posts = Post.objects.all()
    posts = Post.objects.filter(tags__icontains=tag).all()
    featured_post = posts.filter(featured=True).order_by('-updated_on')[0]
    users = User.objects.all().order_by('date_joined')
    categories = Category.objects.all()[:10]
    tags = gen_tags(all_posts, 15)
    
    tag_tup_list = []
    for tag in tags:
        tag_postscount = Post.objects.filter(tags__icontains=tag).all()
        tag_tuple = (tag, len(tag_postscount))
        tag_tup_list.append(tag_tuple)
        
    context = {
        'posts':posts,
        'featured_post':featured_post,
        'tag_tup_list':tag_tup_list,
        'users': users,
        'categories':categories,
        'tag': tag,   
    }
    
    return render(request, 'admin_dashboard/admin_site.html', context)

 
#  admin dashboard selected user's posts view   
@login_required
@user_passes_test(super_user_check)
def admin_dashboard_filter_user_posts_view(request, username):
    all_posts = Post.objects.all()
    posts = Post.objects.filter(author__username=username)
    featured_post = Post.objects.filter(featured=True).order_by('-updated_on')[0]
    users = User.objects.all().order_by('date_joined')
    categories = Category.objects.all()[:10]
    tags = gen_tags(all_posts, 15)
    
    tag_tup_list = []
    for tag in tags:
        tag_postscount = Post.objects.filter(tags__icontains=tag).all()
        tag_tuple = (tag, len(tag_postscount))
        tag_tup_list.append(tag_tuple)
    
    context = {
        'posts':posts,
        'featured_post':featured_post,
        'user': username,
        'users': users,
        'categories':categories,
        'tag_tup_list': tag_tup_list,   
    }
    
    return render(request, 'admin_dashboard/admin_site.html', context)
   
    
#make user as admin view 
@login_required
@user_passes_test(super_user_check)
def make_user_as_admin(request, username):
    user = get_object_or_404(User, username= username)
    
    if not user.is_superuser:
        user.is_stuff = True
        user.is_superuser = True
        user.save()
        return redirect('admim-dashboard')
    else:
        return redirect('admim-dashboard')

#remove user as admin view 
@login_required
@user_passes_test(super_user_check)
def remove_user_admin_as_admin(request, username):
    users = User.objects.all()
    admins = users.filter(is_superuser=True).order_by('date_joined')
    lead_admin = admins[0]
    user = get_object_or_404(User, username= username)
 
    if user.is_superuser and user != lead_admin and user !=request.user:
        user.is_superuser = False
        user.is_stuff = False
        user.save()
        return redirect('admim-dashboard')
    else:
        return redirect('admim-dashboard')

#remove user from database view
@login_required
@user_passes_test(super_user_check)
def remove_user_from_db(request, pk):
    users = User.objects.all()
    admins = users.filter(is_superuser=True).order_by('date_joined')
    lead_admin = admins[0]
    
    if request.method == 'POST':
        user = get_object_or_404(User, pk= pk)
        if user != lead_admin and user !=request.user:
            user.delete()
            return redirect('admim-dashboard')
        else:
            return redirect('admim-dashboard')    

    return render(request, 'admin_dashboard/confirm-delete.html')
        





    


