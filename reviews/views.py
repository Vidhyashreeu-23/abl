from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Review
from .forms import ReviewForm
from clubs.models import Club, Membership


@login_required
def add_review(request, club_slug):
    club = get_object_or_404(Club, slug=club_slug)
    if not Membership.objects.filter(user=request.user, club=club).exists() and not request.user.is_superuser:
        messages.error(request, 'Only members can leave reviews.')
        return redirect('club_detail', slug=club.slug)
    if Review.objects.filter(club=club, user=request.user).exists():
        messages.info(request, 'You have already reviewed this club.')
        return redirect('club_detail', slug=club.slug)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.club = club
            review.user = request.user
            review.save()
            messages.success(request, 'Review submitted.')
            return redirect('club_detail', slug=club.slug)
    else:
        form = ReviewForm()
    return render(request, 'reviews/review_form.html', {'form': form, 'club': club})


@login_required
def edit_review(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if review.user != request.user and not request.user.is_superuser:
        messages.error(request, 'Permission denied.')
        return redirect('club_detail', slug=review.club.slug)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, 'Review updated.')
            return redirect('club_detail', slug=review.club.slug)
    else:
        form = ReviewForm(instance=review)
    return render(request, 'reviews/review_form.html', {'form': form, 'club': review.club, 'review': review})


@login_required
def delete_review(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if review.user != request.user and not request.user.is_superuser:
        messages.error(request, 'Permission denied.')
        return redirect('club_detail', slug=review.club.slug)
    if request.method == 'POST':
        club_slug = review.club.slug
        review.delete()
        messages.success(request, 'Review deleted.')
        return redirect('club_detail', slug=club_slug)
    return render(request, 'reviews/review_form.html', {'form': ReviewForm(instance=review), 'club': review.club, 'review': review})
