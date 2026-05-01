from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Post, Comment
from .forms import PostForm, CommentForm
from clubs.models import Club, Membership


def post_list(request, club_slug):
    club = get_object_or_404(Club, slug=club_slug)
    posts = Post.objects.filter(club=club).order_by('-is_pinned', '-created_at')
    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    posts_page = paginator.get_page(page)
    return render(request, 'posts/post_list.html', {'club': club, 'posts': posts_page})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.select_related('author')
    comment_form = CommentForm()
    return render(request, 'posts/post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
    })


@login_required
def create_post(request, club_slug):
    club = get_object_or_404(Club, slug=club_slug)
    if not Membership.objects.filter(user=request.user, club=club, role__in=['admin', 'president']).exists() and not request.user.is_superuser:
        messages.error(request, 'Only club admins can create posts.')
        return redirect('club_detail', slug=club.slug)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.club = club
            post.author = request.user
            post.save()
            messages.success(request, 'Post created successfully.')
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'posts/create_post.html', {'form': form, 'club': club})


@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user and not Membership.objects.filter(user=request.user, club=post.club, role__in=['admin', 'president']).exists() and not request.user.is_superuser:
        messages.error(request, 'Permission denied.')
        return redirect('post_detail', pk=post.pk)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully.')
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'posts/create_post.html', {'form': form, 'post': post})


@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user and not Membership.objects.filter(user=request.user, club=post.club, role__in=['admin', 'president']).exists() and not request.user.is_superuser:
        messages.error(request, 'Permission denied.')
        return redirect('post_detail', pk=post.pk)
    if request.method == 'POST':
        club_slug = post.club.slug
        post.delete()
        messages.success(request, 'Post deleted successfully.')
        return redirect('post_list', club_slug=club_slug)
    return render(request, 'posts/post_detail.html', {'post': post, 'comments': post.comments.all(), 'comment_form': CommentForm()})


@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    club = post.club
    if not Membership.objects.filter(user=request.user, club=club).exists() and not request.user.is_superuser:
        messages.error(request, 'Only club members can comment.')
        return redirect('post_detail', pk=post.pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Comment added.')
    return redirect('post_detail', pk=post.pk)
