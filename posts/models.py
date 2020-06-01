from django.db import models
from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from django.core.validators import RegexValidator

# for hitcount
from django.contrib.contenttypes.fields import GenericRelation
from hitcount.models import HitCount, HitCountMixin
# django resize package
from django_resized import ResizedImageField


User = get_user_model()

# Categories model for Categorize every post
class Category(models.Model):
    category = models.CharField(max_length=20)

    def get_absolute_url(self):
        return reverse('posts_in_category', kwargs={
            'id': self.id
        })

    def __str__(self):
        return self.category
    
    def save(self, *args, **kwargs):
        if self.category:
            self.category = self.category.capitalize()

        super(Category, self).save(*args, **kwargs)
    

only_aphabets =  RegexValidator(r'^[, a-zA-Z]*$', 'Enter comma separated tags. (use space for two words tag)')
# post model, used 3rd party- hitcount
class Post(models.Model):
    
    # parent fields
    categories = models.ManyToManyField(Category)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # blog-specific field
    title = models.CharField(max_length=100)
    post_thumbnail = ResizedImageField(size=[900, 600], crop=['middle', 'center'], quality=90, keep_meta=False, upload_to='posts_image', default ='default.jpg', force_format='JPEG')
    tags = models.CharField(max_length=60, blank=True, validators=[only_aphabets])
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now= True)
    content = models.TextField()
    featured = models.BooleanField()

    # 3rd party field
    hit_count = GenericRelation(
                HitCount, object_id_field='object_pk',
                related_query_name='hit_count_generic_relation')

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title
    
    # preprossesing before save
    def save(self, *args, **kwargs):
        if not self.tags:
            self.tags = 'blog,programming'.capitalize()
        else:
            self.tags = self.tags.capitalize()
            
        super(Post, self).save(*args, **kwargs)
        
    # delete everything when delete this model 
    def delete(self, *args, **kwargs):
        self.post_thumbnail.delete()
        
        return super(Post, self).delete(*args, **kwargs)
    
    # func for getting absoulute url of this post
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={
            'pk': self.pk
        })

    @property
    def get_all_comments(self):
        return self.comments.all().order_by('comment_time')
   
    @property
    def get_comments_count(self):
        return self.comments.all().count()

