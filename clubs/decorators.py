from functools import wraps
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Club, Membership


def club_admin_required(view_func):
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        club = get_object_or_404(Club, slug=kwargs.get('slug') or kwargs.get('club_slug'))
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        membership = Membership.objects.filter(user=request.user, club=club, role__in=['admin', 'president']).first()
        if membership:
            return view_func(request, *args, **kwargs)
        messages.error(request, 'You must be a club admin or president to access that page.')
        return redirect('club_detail', slug=club.slug)
    return _wrapped_view
