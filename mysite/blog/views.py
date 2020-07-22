from django.shortcuts import render,get_object_or_404,redirect
from django.utils import timezone
from django.views.generic import View, TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from blog.models import Post, Comment
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from blog.forms import PostForm, CommentForm
from django.urls import reverse_lazy

# Create your views here.
class AboutView(TemplateView):
     template_name = 'about.html'


class PostListView(ListView):
    model=Post

    def get_queryset(self):
        # this get_queryset gives us the list of objects based on some filters that we want

        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

        # here __ helps python understand that lte (less than equal to ) is a sql Function
        # above statement just means that i want a query of Post based on published date less than or equal to current  timezone

class PostDetailView(DetailView):
    model=Post


class PostCreateView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    # here i am providing the login page and after the login is successfull i am redirecting it to some other page
    form_class=PostForm
    model = Post


class PostUpdateView(LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    # here i am providing the login page and after the login is successfull i am redirecting it to some other page
    form_class=PostForm
    model = Post

class PostDeleteView(LoginRequiredMixin,DeleteView):
    model=Post
    success_url=reverse_lazy('post_list')


class DraftListView(LoginRequiredMixin,ListView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'

    model=Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('create_date')

################################
################################
################################

@login_required
def post_publish(request,pk):
    post=get_object_or_404(Post,pk=pk)
    post.publish()
    return redirect('post_detail',pk=post.pk)





@login_required
def add_comment_to_post(request,pk):
    post=get_object_or_404(Post,pk=pk)
    if request.method == 'POST':
        form=CommentForm(request.POST)
        if form.is_valid():
            comment=form.save(commit=False)
            comment.post=post
            comment.save()
            return redirect('post_detail',pk=post.pk)
    else:
        form = CommentForm()
    return render  (request,'blog/comment_form.html',{'form':form})

# post is also an attribute of comment so  i am saving that post to that attribute of comment
# get_object_or_404 either gives you the model instance or if it could not find return error

@login_required
def comment_approve(request,pk):
    comment=get_object_or_404(Comment,pk=pk)
    comment.approve()
    return redirect('post_detail',pk=comment.post.pk)


@login_required
def comment_remove(request,pk):
    comment=get_object_or_404(Comment,pk=pk)
    post_pk=comment.post.pk
    comment.delete()
    return redirect('post_detail',pk=post_pk)

# after deletion it is going to forget its pk so i saved it before deleting
