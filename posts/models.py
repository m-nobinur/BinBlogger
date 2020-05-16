from django.db import models
from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from django.core.validators import RegexValidator

from tinymce import models as tinymce_models

# for hitcount
from django.contrib.contenttypes.fields import GenericRelation
from hitcount.models import HitCount, HitCountMixin


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


# post model, used 3rd party- hitcount
POST_STATUS = (
    (0,"Draft"),
    (1,"Publish")
    )
only_aphabets =  RegexValidator(r'^[ a-zA-Z]*$', 'Only space separate English letters are allowed.')

class Post(models.Model):

    # parent fields
    categories = models.ManyToManyField(Category)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # blog-specific field
    title = models.CharField(max_length=100)
    post_thumbnail = models.ImageField(upload_to='posts_image', default ='default.jpg')
    tags = models.CharField(max_length=40, blank=True, validators=[only_aphabets])
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now= True)
    content = tinymce_models.HTMLField()
    featured = models.BooleanField()
    status = models.IntegerField(choices=POST_STATUS, default=0)

    # 3rd party field
    hit_count = GenericRelation(
                HitCount, object_id_field='object_pk',
                related_query_name='hit_count_generic_relation')


    class Meta:
        ordering = ['-created_on']

    # previous_post = models.ForeignKey(
    #     'self', related_name='previous', on_delete=models.SET_NULL, blank=True, null=True)
    # next_post = models.ForeignKey(
    #     'self', related_name='next', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.tags:
            self.tags = 'blog programming'.upper()
        else:
            self.tags = self.tags.upper()
        return super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={
            'pk': self.pk
        })

    # def get_update_url(self):
    #     return reverse('post-update', kwargs={
    #         'pk': self.pk
    #     })

    # def get_delete_url(self):
    #     return reverse('post-delete', kwargs={
    #         'pk': self.pk
    #     })

    # @property
    # def get_comments(self):
    #     return self.comments.all().order_by('-timestamp')

    # @property
    # def comment_count(self):
    #     return Comment.objects.filter(post=self).count()

    # @property
    # def view_count(self):
    #     return PostView.objects.filter(post=self).count()
