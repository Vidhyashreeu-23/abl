from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from .models import Event, EventRegistration
from .forms import EventForm
from clubs.models import Club, Membership


def event_list(request):
    q = request.GET.get('q', '')
    club_slug = request.GET.get('club', '')
    date_filter = request.GET.get('date', '')
    events = Event.objects.filter(start_datetime__gte=timezone.now()).select_related('club')
    if q:
        events = events.filter(Q(title__icontains=q) | Q(description__icontains=q) | Q(club__name__icontains=q))
    if club_slug:
        events = events.filter(club__slug=club_slug)
    if date_filter:
        events = events.filter(start_datetime__date=date_filter)
    paginator = Paginator(events.order_by('start_datetime'), 9)
    page = request.GET.get('page')
    events_page = paginator.get_page(page)
    return render(request, 'events/event_list.html', {
        'events': events_page,
        'q': q,
        'club_slug': club_slug,
        'date_filter': date_filter,
    })


def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    is_registered = False
    can_manage_event = False
    if request.user.is_authenticated:
        is_registered = EventRegistration.objects.filter(event=event, user=request.user).exists()
        can_manage_event = _user_can_manage_event(request.user, event)
    return render(request, 'events/event_detail.html', {
        'event': event,
        'is_registered': is_registered,
        'can_manage_event': can_manage_event,
    })


def _user_can_manage_event(user, event):
    if user.is_superuser:
        return True
    return Membership.objects.filter(user=user, club=event.club, role__in=['admin', 'president']).exists()


@login_required
def create_event(request, club_slug):
    club = get_object_or_404(Club, slug=club_slug)
    if not Membership.objects.filter(user=request.user, club=club, role__in=['admin', 'president']).exists() and not request.user.is_superuser:
        messages.error(request, 'Only club admins can create events.')
        return redirect('club_detail', slug=club.slug)
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.club = club
            event.created_by = request.user
            event.save()
            messages.success(request, 'Event created successfully.')
            return redirect('event_detail', pk=event.pk)
    else:
        form = EventForm()
    return render(request, 'events/create_event.html', {'form': form, 'club': club})


@login_required
def edit_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if not _user_can_manage_event(request.user, event):
        messages.error(request, 'You do not have permission to edit this event.')
        return redirect('event_detail', pk=event.pk)
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event updated successfully.')
            return redirect('event_detail', pk=event.pk)
    else:
        form = EventForm(instance=event)
    return render(request, 'events/edit_event.html', {'form': form, 'event': event})


@login_required
def delete_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if not _user_can_manage_event(request.user, event):
        messages.error(request, 'You do not have permission to delete this event.')
        return redirect('event_detail', pk=event.pk)
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Event deleted successfully.')
        return redirect('event_list')
    return redirect('event_detail', pk=event.pk)


@login_required
def register_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        registration, created = EventRegistration.objects.get_or_create(event=event, user=request.user)
        if created:
            messages.success(request, 'You are registered for the event.')
        else:
            registration.delete()
            messages.success(request, 'Your registration has been canceled.')
    return redirect('event_detail', pk=event.pk)


@login_required
def my_events(request):
    registrations = EventRegistration.objects.filter(user=request.user).select_related('event')
    return render(request, 'events/my_events.html', {'registrations': registrations})
