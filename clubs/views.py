from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count, Avg
from django.utils import timezone
from .models import Club, Category, Membership
from .forms import ClubForm
from posts.models import Post
from events.models import Event
from reviews.models import Review
from .decorators import club_admin_required


def club_list(request):
    q = request.GET.get('q', '')
    category_slug = request.GET.get('category', '')
    clubs = Club.objects.filter(is_approved=True).select_related('category')
    if q:
        clubs = clubs.filter(Q(name__icontains=q) | Q(category__name__icontains=q))
    if category_slug:
        clubs = clubs.filter(category__slug=category_slug)
    clubs = clubs.annotate(member_count_agg=Count('memberships', distinct=True), avg_rating=Avg('reviews__rating'))
    categories = Category.objects.all()
    paginator = Paginator(clubs.order_by('name'), 12)
    page = request.GET.get('page')
    clubs_page = paginator.get_page(page)
    return render(request, 'clubs/club_list.html', {
        'clubs': clubs_page,
        'categories': categories,
        'q': q,
        'category_slug': category_slug,
    })


def club_detail(request, slug):
    club = get_object_or_404(Club, slug=slug)
    posts = Post.objects.filter(club=club).order_by('-is_pinned', '-created_at')[:10]
    events = Event.objects.filter(club=club, start_datetime__gte=timezone.now()).order_by('start_datetime')[:5]
    members = Membership.objects.filter(club=club).select_related('user')
    reviews = Review.objects.filter(club=club).order_by('-created_at')[:10]
    review_form = None
    if request.user.is_authenticated:
        from reviews.forms import ReviewForm
        review_form = ReviewForm()
    return render(request, 'clubs/club_detail.html', {
        'club': club,
        'posts': posts,
        'events': events,
        'members': members,
        'reviews': reviews,
        'review_form': review_form,
    })


@login_required
def create_club(request):
    if request.method == 'POST':
        form = ClubForm(request.POST, request.FILES)
        if form.is_valid():
            club = form.save(commit=False)
            club.created_by = request.user
            club.save()
            form.save_m2m()
            messages.success(request, 'Club created successfully.')
            return redirect('club_detail', slug=club.slug)
    else:
        form = ClubForm()
    return render(request, 'clubs/create_club.html', {'form': form})


@club_admin_required
def edit_club(request, slug):
    club = get_object_or_404(Club, slug=slug)
    if request.method == 'POST':
        form = ClubForm(request.POST, request.FILES, instance=club)
        if form.is_valid():
            form.save()
            messages.success(request, 'Club updated successfully.')
            return redirect('club_detail', slug=club.slug)
    else:
        form = ClubForm(instance=club)
    return render(request, 'clubs/edit_club.html', {'form': form, 'club': club})


@club_admin_required
def delete_club(request, slug):
    club = get_object_or_404(Club, slug=slug)
    if request.method == 'POST':
        club.delete()
        messages.success(request, 'Club deleted successfully.')
        return redirect('club_list')
    return redirect('club_detail', slug=club.slug)


@login_required
def join_club(request, slug):
    club = get_object_or_404(Club, slug=slug)
    if request.method == 'POST':
        membership, created = Membership.objects.get_or_create(user=request.user, club=club)
        if created:
            messages.success(request, f'You joined {club.name}.')
        else:
            messages.info(request, 'You are already a member of this club.')
    return redirect('club_detail', slug=club.slug)


@login_required
def leave_club(request, slug):
    club = get_object_or_404(Club, slug=slug)
    if request.method == 'POST':
        Membership.objects.filter(user=request.user, club=club).exclude(role='president').delete()
        messages.success(request, f'You left {club.name}.')
    return redirect('club_detail', slug=club.slug)


def member_list(request, slug):
    club = get_object_or_404(Club, slug=slug)
    members = Membership.objects.filter(club=club).select_related('user')
    return render(request, 'clubs/member_list.html', {'club': club, 'members': members})


@login_required
def my_clubs(request):
    memberships = Membership.objects.filter(user=request.user).select_related('club')
    return render(request, 'clubs/my_clubs.html', {'memberships': memberships})
