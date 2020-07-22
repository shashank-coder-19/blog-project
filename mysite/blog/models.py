from django.db import models
from django.urls import reverse
from django.utils import timezone
# Create your models here.
class Post(models.Model):
    author=models.ForeignKey('auth.user',on_delete=models.CASCADE)
    # here i am connecting author to an actual user
    title=models.CharField(max_length=200)
    text=models.TextField()
    create_date=models.DateTimeField(default=timezone.now())
    published_date=models.DateTimeField(blank=True,null=True)
    # author may not publish the post at same time when it creates or it may so that is why i am using blank and null

    def publish(self):
        self.published_date=timezone.now()
        self.save()
        # it saves the time when the author publish the Post

    def __str__(self):
        return self.title

    def approve_comments(self):
        return self.comments.filter(approved_comment=True)

    def get_absolute_url(self):
        return reverse('post_detail',kwargs={'pk':self.pk})

    # here i want to return to detail page of that particular post

class Comment(models.Model):
    post=models.ForeignKey('Post',related_name='comments',on_delete=models.CASCADE)
    author=models.CharField(max_length=200)
    text=models.TextField()
    create_date=models.DateTimeField(default=timezone.now())
    approved_comment=models.BooleanField(default=False)
    # here default shows that comments are not approved initially
    def approve(self):
        self.approved_comment=True
        self.save()


    def get_absolute_url(self):
        return reverse('post_list')

    # here i want to return to homepage only

    def __str__(self):
        return self.text
