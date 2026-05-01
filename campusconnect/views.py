from django.shortcuts import render
from clubs.models import Club
from events.models import Event
from django.db.models import Count, Avg
from django.utils import timezone


def home(request):
    featured_clubs = Club.objects.annotate(review_count_agg=Count('reviews'), avg_rating=Avg('reviews__rating')).order_by('-avg_rating')[:6]
    upcoming_events = Event.objects.filter(start_datetime__gte=timezone.now()).order_by('start_datetime')[:3]
    total_clubs = Club.objects.count()
    total_members = Club.objects.aggregate(total=Count('memberships__user', distinct=True))['total'] or 0
    total_events = Event.objects.count()
    return render(request, 'home.html', {
        'featured_clubs': featured_clubs,
        'upcoming_events': upcoming_events,
        'total_clubs': total_clubs,
        'total_members': total_members,
        'total_events': total_events,
    })
