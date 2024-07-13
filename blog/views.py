from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponseForbidden
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from users.decorators import roles_allowed

def is_author_or_admin(user, post):
    return user == post.author or user.is_superuser or user.role == "admin"

@login_required
@roles_allowed(['author', 'admin', 'reader'])
def post_list(request):
    if request.user.role == 'admin':
        posts = Post.objects.all().order_by('-created_at')
    elif request.user.role == 'author':
        posts = Post.objects.filter(author=request.user).order_by('-created_at')
    else:
        posts = Post.objects.filter(status='published')
    return render(request, 'blog/home.html', {'posts': posts})

@login_required
@roles_allowed(['author', 'admin', 'reader'])
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

@login_required
@roles_allowed(['author', 'admin'])
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})

@login_required
@roles_allowed(['author', 'admin'])
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if not is_author_or_admin(request.user, post):
        return HttpResponseForbidden("You do not have permission to edit this post.")
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form})

@login_required
@roles_allowed(['author', 'admin'])
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if not is_author_or_admin(request.user, post):
        return HttpResponseForbidden("You do not have permission to delete this post.")
    if request.method == 'POST':
        post.delete()
        return redirect('home')
    return render(request, 'blog/post_confirm_delete.html', {'post': post})

@login_required
@roles_allowed(['author', 'admin', 'reader'])
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form, 'post': post})

@login_required
@roles_allowed(['admin'])
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == 'POST':
        comment.delete()
        return redirect('post_detail', pk=comment.post.pk)
    return render(request, 'blog/comment_confirm_delete.html', {'comment': comment})